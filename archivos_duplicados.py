import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import hashlib

def buscar_archivos_duplicados(carpeta, text_widget, stats_widget, ventana):
    """
    Busca archivos duplicados y actualiza el widget de texto con el progreso y estadísticas.
    """
    hashes = {}
    archivos_analizados = 0
    duplicados_detectados = 0

    text_widget.insert(tk.END, f"Iniciando búsqueda en la carpeta: {carpeta}\n")
    text_widget.see(tk.END)
    ventana.update()  # Actualiza la interfaz gráfica

    for root, _, files in os.walk(carpeta):
        text_widget.insert(tk.END, f"Analizando carpeta: {root}\n")
        text_widget.see(tk.END)
        ventana.update()
        for file in files:
            if file.lower() == "desktop.ini":
                text_widget.insert(tk.END, f"Omitiendo archivo: {file}\n")
                text_widget.see(tk.END)
                ventana.update()
                continue

            ruta_archivo = os.path.join(root, file)
            text_widget.insert(tk.END, f"Procesando archivo: {ruta_archivo}\n")
            text_widget.see(tk.END)
            ventana.update()

            if os.path.getsize(ruta_archivo) == 0:
                text_widget.insert(tk.END, f"Archivo vacío detectado: {ruta_archivo}\n")
                text_widget.see(tk.END)
                ventana.update()
                continue

            archivos_analizados += 1
            hash_archivo = calcular_hash(ruta_archivo, text_widget, ventana)

            if hash_archivo in hashes:
                if os.path.getsize(hashes[hash_archivo][0]) == os.path.getsize(ruta_archivo):
                    hashes[hash_archivo].append(ruta_archivo)
                    text_widget.insert(tk.END, f"Duplicado detectado: {ruta_archivo}\n")
                    duplicados_detectados += 1
                else:
                    text_widget.insert(tk.END, f"Conflicto: {ruta_archivo} tiene el mismo hash pero diferente tamaño.\n")
            else:
                hashes[hash_archivo] = [ruta_archivo]

            # Actualizar estadísticas en tiempo real
            stats_widget.delete(1.0, tk.END)
            stats_widget.insert(tk.END, f"Archivos analizados: {archivos_analizados}\n")
            stats_widget.insert(tk.END, f"Duplicados detectados: {duplicados_detectados}\n")
            stats_widget.see(tk.END)
            ventana.update()

    duplicados = {hash_: rutas for hash_, rutas in hashes.items() if len(rutas) > 1}
    text_widget.insert(tk.END, "Búsqueda completada.\n")
    text_widget.see(tk.END)
    ventana.update()
    return duplicados

def calcular_hash(ruta_archivo, text_widget, ventana, buffer_size=65536):
    """
    Calcula el hash SHA-256 de un archivo y actualiza el widget de texto con el progreso.
    """
    hash_sha256 = hashlib.sha256()
    try:
        with open(ruta_archivo, 'rb') as archivo:
            while chunk := archivo.read(buffer_size):
                hash_sha256.update(chunk)
    except Exception as e:
        text_widget.insert(tk.END, f"Error al procesar el archivo {ruta_archivo}: {e}\n")
        text_widget.see(tk.END)
        ventana.update()
    return hash_sha256.hexdigest()

def mostrar_opciones_eliminacion(duplicados, text_widget, ventana):
    """
    Muestra opciones de eliminación después de obtener los duplicados.
    """
    opcion_var = tk.StringVar(value="no_eliminar")

    def realizar_eliminacion():
        opcion = opcion_var.get()
        archivos_eliminados = []
        archivos_permanecen = []
        espacio_ahorrado = 0
        if opcion == "no_eliminar":
            text_widget.insert(tk.END, "No se eliminaron archivos.\n")
        elif opcion == "todos":
            archivos_eliminados, archivos_permanecen, espacio_ahorrado = eliminar_duplicados(
                duplicados, text_widget, ventana, opcion="todos"
            )
        elif opcion == "uno_a_uno":
            archivos_eliminados, archivos_permanecen, espacio_ahorrado = eliminar_duplicados(
                duplicados, text_widget, ventana, opcion="uno_a_uno"
            )

        # Mostrar resumen de archivos eliminados y los que permanecen
        resumen_eliminacion_widget.config(state=tk.NORMAL)
        resumen_eliminacion_widget.delete(1.0, tk.END)
        resumen_eliminacion_widget.insert(tk.END, f"Espacio ahorrado: {espacio_ahorrado / (1024 * 1024):.2f} MB\n")
        resumen_eliminacion_widget.insert(tk.END, "\nResumen de archivos eliminados:\n")
        for archivo in archivos_eliminados:
            resumen_eliminacion_widget.insert(tk.END, f"  - {archivo}\n")
        resumen_eliminacion_widget.insert(tk.END, "\nArchivos que permanecen:\n")
        for archivo in archivos_permanecen:
            resumen_eliminacion_widget.insert(tk.END, f"  - {archivo}\n")
        resumen_eliminacion_widget.config(state=tk.DISABLED)

    top = tk.Toplevel(ventana)
    top.title("Opciones de eliminación")
    top.geometry("1200x700")

    tk.Label(top, text="Seleccione cómo manejar los duplicados:", font=("Arial", 12)).pack(pady=10)

    opciones_frame = tk.Frame(top)
    opciones_frame.pack(pady=10)

    # Cargar iconos
    icono_no_eliminar = ImageTk.PhotoImage(Image.open("icono_no_eliminar.png").resize((40, 40)))
    icono_eliminar_todos = ImageTk.PhotoImage(Image.open("icono_eliminar_todos.png").resize((60, 40)))
    icono_eliminar_uno = ImageTk.PhotoImage(Image.open("icono_eliminar_uno.png").resize((60, 40)))

    tk.Radiobutton(opciones_frame, text=" No eliminar", image=icono_no_eliminar, compound="left", variable=opcion_var, value="no_eliminar").pack(side="left", padx=10)
    tk.Radiobutton(opciones_frame, text=" Eliminar todos", image=icono_eliminar_todos, compound="left", variable=opcion_var, value="todos").pack(side="left", padx=10)
    tk.Radiobutton(opciones_frame, text=" Eliminar uno por uno", image=icono_eliminar_uno, compound="left", variable=opcion_var, value="uno_a_uno").pack(side="left", padx=10)

    resumen_widget = scrolledtext.ScrolledText(top, width=100, height=20, font=("Consolas", 10))
    resumen_widget.pack(pady=10, fill=tk.BOTH, expand=True)
    resumen_widget.insert(tk.END, "Resumen de archivos duplicados:\n\n")
    for hash_, archivos in duplicados.items():
        resumen_widget.insert(tk.END, f"Hash: {hash_}\n")
        for archivo in archivos:
            resumen_widget.insert(tk.END, f"  - {archivo}\n")
    resumen_widget.config(state=tk.DISABLED)

    resumen_eliminacion_widget = scrolledtext.ScrolledText(top, width=100, height=10, font=("Consolas", 10))
    resumen_eliminacion_widget.pack(pady=10, fill=tk.BOTH, expand=True)
    resumen_eliminacion_widget.insert(tk.END, "Resumen de archivos eliminados:\n")
    resumen_eliminacion_widget.config(state=tk.DISABLED)

    botones_frame = tk.Frame(top)
    botones_frame.pack(pady=10)

    tk.Button(botones_frame, text="Confirmar", command=realizar_eliminacion, bg="green", fg="white").pack(side="left", padx=10)
    tk.Button(botones_frame, text="Cerrar", command=top.destroy, bg="red", fg="white").pack(side="left", padx=10)

    # Mantener referencias para los iconos
    top.icono_no_eliminar = icono_no_eliminar
    top.icono_eliminar_todos = icono_eliminar_todos
    top.icono_eliminar_uno = icono_eliminar_uno

def eliminar_duplicados(duplicados, text_widget, ventana, opcion):
    """
    Maneja la eliminación de duplicados según la opción seleccionada.
    Devuelve listas de archivos eliminados, archivos que permanecen y el espacio ahorrado.
    """
    archivos_eliminados = []
    archivos_permanecen = []
    espacio_ahorrado = 0

    def eliminar_todos():
        nonlocal espacio_ahorrado
        for hash_, archivos in duplicados.items():
            archivos = sorted(archivos, key=lambda x: ("copia" in os.path.basename(x).lower(), x))
            archivos_permanecen.append(archivos[0])
            for archivo in archivos[1:]:
                try:
                    espacio_ahorrado += os.path.getsize(archivo)
                    os.remove(archivo)
                    archivos_eliminados.append(archivo)
                    text_widget.insert(tk.END, f"Archivo eliminado: {archivo}\n")
                except Exception as e:
                    text_widget.insert(tk.END, f"Error al eliminar {archivo}: {e}\n")
        text_widget.insert(tk.END, "Todos los duplicados han sido eliminados.\n")
        text_widget.see(tk.END)
        ventana.update()

    def eliminar_individual():
        nonlocal espacio_ahorrado
        for hash_, archivos in duplicados.items():
            archivos = sorted(archivos, key=lambda x: ("copia" in os.path.basename(x).lower(), x))
            archivos_permanecen.append(archivos[0])
            for archivo in archivos[1:]:
                respuesta = messagebox.askyesno("Eliminar archivo", f"¿Eliminar este archivo duplicado?\n{archivo}")
                if respuesta:
                    try:
                        espacio_ahorrado += os.path.getsize(archivo)
                        os.remove(archivo)
                        archivos_eliminados.append(archivo)
                        text_widget.insert(tk.END, f"Archivo eliminado: {archivo}\n")
                    except Exception as e:
                        text_widget.insert(tk.END, f"Error al eliminar {archivo}: {e}\n")
        text_widget.insert(tk.END, "Eliminación interactiva completada.\n")
        text_widget.see(tk.END)
        ventana.update()

    if opcion == "todos":
        eliminar_todos()
    elif opcion == "uno_a_uno":
        eliminar_individual()

    return archivos_eliminados, archivos_permanecen, espacio_ahorrado

def ejecutar_busqueda():
    """
    Ejecuta la búsqueda de duplicados y muestra el progreso en la interfaz.
    """
    carpeta = filedialog.askdirectory(title="Seleccione una carpeta para analizar")
    if not carpeta:
        messagebox.showwarning("Advertencia", "No se seleccionó ninguna carpeta.")
        return

    text_widget.delete(1.0, tk.END)
    stats_widget.delete(1.0, tk.END)
    duplicados = buscar_archivos_duplicados(carpeta, text_widget, stats_widget, ventana)

    if duplicados:
        resultado = f"Se encontraron {len(duplicados)} grupos de duplicados:\n\n"
        for hash_, archivos in duplicados.items():
            resultado += f"Hash: {hash_}\n"
            for archivo in archivos:
                resultado += f"  - {archivo}\n"
        text_widget.insert(tk.END, "\nResumen de duplicados:\n")
        text_widget.insert(tk.END, resultado)
        text_widget.see(tk.END)
        ventana.update()

        mostrar_opciones_eliminacion(duplicados, text_widget, ventana)
    else:
        text_widget.insert(tk.END, "No se encontraron archivos duplicados.\n")
        messagebox.showinfo("Resultados", "No se encontraron archivos duplicados.")

ventana = tk.Tk()
ventana.title("Búsqueda de Archivos Duplicados")
ventana.geometry("800x700")

label = tk.Label(ventana, text="Seleccione una carpeta para buscar archivos duplicados", font=("Arial", 12))
label.pack(pady=10)

boton_buscar = tk.Button(ventana, text="Buscar Archivos Duplicados", command=ejecutar_busqueda, font=("Arial", 12))
boton_buscar.pack(pady=10)

text_frame = tk.Frame(ventana)
text_frame.pack(pady=10, fill=tk.BOTH, expand=True)

text_label = tk.Label(text_frame, text="Progreso de la búsqueda:", font=("Arial", 10))
text_label.pack(anchor="w")

text_widget = scrolledtext.ScrolledText(text_frame, width=80, height=20, font=("Consolas", 10))
text_widget.pack(pady=5, fill=tk.BOTH, expand=True)

stats_frame = tk.Frame(ventana)
stats_frame.pack(pady=10, fill=tk.BOTH, expand=True)

stats_label = tk.Label(stats_frame, text="Estadísticas en tiempo real:", font=("Arial", 10))
stats_label.pack(anchor="w")

stats_widget = scrolledtext.ScrolledText(stats_frame, width=80, height=4, font=("Consolas", 10))
stats_widget.pack(pady=5, fill=tk.BOTH, expand=True)

boton_salir = tk.Button(ventana, text="Salir", command=ventana.quit, font=("Arial", 12), bg="red", fg="white")
boton_salir.pack(pady=10)

ventana.mainloop()
