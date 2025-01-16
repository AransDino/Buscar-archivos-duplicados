
# Herramienta de Búsqueda de Archivos Duplicados

## Descripción General
Esta herramienta es una aplicación gráfica en Python que permite localizar y gestionar archivos duplicados en una carpeta seleccionada. Utiliza un enfoque basado en hashes para identificar duplicados con precisión y ofrece opciones flexibles para su gestión.

---

## Características
- **Escaneo Recursivo de Directorios:** Analiza todos los archivos dentro de la carpeta seleccionada y sus subcarpetas.
- **Detección de Duplicados Basada en Hashes:** Utiliza SHA-256 para identificar archivos duplicados con precisión.
- **Actualización en Tiempo Real:** Muestra el progreso del análisis y las estadísticas directamente en la interfaz gráfica.
- **Gestión de Duplicados:**
  - Mantener todos los archivos duplicados.
  - Eliminar automáticamente duplicados, manteniendo solo una copia.
  - Revisar los duplicados de forma interactiva para eliminarlos selectivamente.
- **Interfaz Amigable:** Construida con `Tkinter`, ofrece una experiencia de usuario fluida e intuitiva.

---

## Requisitos Previos
- **Python** 3.8 o superior.
- Dependencias necesarias:
  - `tkinter` (incluido en la biblioteca estándar de Python).
  - `Pillow` para el manejo de imágenes.

---

## Instalación

### Clonar el repositorio:
```bash
git clone https://github.com/AransDino/Buscar-archivos-duplicados.git
```

### Instalar las dependencias necesarias:
```bash
pip install pillow
```

### Ejecutar la aplicación:
```bash
python archivos_duplicados.py
```

---

## Instrucciones de Uso
1. Ejecutar la aplicación.
2. Hacer clic en el botón **"Buscar Archivos Duplicados"** para abrir el selector de carpetas.
3. Seleccionar la carpeta que se desea analizar.
4. Ver el progreso del análisis y las estadísticas en tiempo real.
5. Al finalizar el análisis:
   - Revisar la lista de duplicados en el resumen.
   - Elegir una opción de gestión:
     - Mantener todos los archivos.
     - Eliminar automáticamente todos los duplicados.
     - Eliminar duplicados uno por uno con confirmación.
6. Consultar el resumen final con el espacio ahorrado y los archivos gestionados.

---

## Estructura del Proyecto
- **`herramienta_archivos_duplicados.py`**: Archivo principal con el código de la aplicación.
- **Recursos**:
  - `icono_no_eliminar.png`: Icono para la opción "No eliminar".
  - `icono_eliminar_todos.png`: Icono para la opción "Eliminar todos".
  - `icono_eliminar_uno.png`: Icono para la opción "Eliminar uno por uno".

---

## Funciones Principales
### `buscar_archivos_duplicados(carpeta, text_widget, stats_widget, ventana)`
Escanea la carpeta seleccionada para encontrar archivos duplicados, actualizando los widgets de texto y estadísticas en tiempo real.

### `calcular_hash(ruta_archivo, text_widget, ventana)`
Genera el hash SHA-256 de un archivo para identificar duplicados.

### `mostrar_opciones_eliminacion(duplicados, text_widget, ventana)`
Muestra las opciones para gestionar los duplicados encontrados.

### `eliminar_duplicados(duplicados, text_widget, ventana, opcion)`
Elimina archivos duplicados según la opción seleccionada por el usuario (mantener, eliminar automáticamente, eliminar uno por uno).

---

## Capturas de Pantalla
### Interfaz Principal
![image](https://github.com/user-attachments/assets/5a422f40-ba6c-4614-9407-9c0f7934cfa4)

### Opciones de Gestión de Duplicados
![image](https://github.com/user-attachments/assets/e3b2b845-ec9a-4ee3-a940-3139b1fdcf16)

---

## Mejoras Futuras
- Soporte para múltiples idiomas.
- Registro de eventos (logging) para depuración y auditoría.
- Optimización del cálculo de hashes mediante hilos para manejar grandes volúmenes de archivos.

---

## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulte el archivo `LICENSE` para más detalles.

---

## Contribuciones
¡Las contribuciones son bienvenidas! Realiza un fork del repositorio, crea un branch con tus cambios y envía un pull request. Asegúrate de seguir los estándares de codificación de PEP 8.

---

¡Gracias por usar la Herramienta de Búsqueda de Archivos Duplicados! 😊
