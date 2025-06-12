"""
Script para exportar automáticamente los estilos (.qml) de todas las capas de un proyecto QGIS.

 ¿Qué hace?
    - Recorre todas las capas cargadas en el proyecto actual
    - Guarda el estilo (simbología) de cada capa como un archivo `.qml`
    - Los archivos se guardan en la ruta especificada

 Cómo usar:
    1. Abrir un proyecto en QGIS con las capas cargadas
    2. Modificar la variable `ruta_destino` con la carpeta de destino deseada
    3. Ejecutar este script desde la consola de Python en QGIS

 Requisitos:
    - QGIS 3.x
    - Capas con simbología definida

Autor: 95devFran (GitHub: https://github.com/95devFran)
"""

import os
from qgis.core import QgsProject

# Ruta donde quieres guardar los archivos .qml (básicamente es la simbología)
ruta_destino = r'C:/ruta/de/salida/para/qml' 

# Crear la carpeta si no existe
os.makedirs(ruta_destino, exist_ok=True)

# Iterar por todas las capas del proyecto
for capa in QgsProject.instance().mapLayers().values():
    nombre = capa.name()
    archivo_qml = os.path.join(ruta_destino, f"{nombre}.qml")

    # Guardar el estilo de la capa como archivo .qml
    capa.saveNamedStyle(archivo_qml)

    print(f" Estilo de '{nombre}' guardado en: {archivo_qml}")

print("✔ Exportación de estilos completada.")
