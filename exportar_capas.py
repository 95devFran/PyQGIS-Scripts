"""
Script para exportar automáticamente todas las capas cargadas en QGIS a archivos Shapefile (.shp).

¿Qué hace?
    - Recorre todas las capas visibles en el panel de capas del proyecto actual
    - Exporta cada capa como un archivo .shp individual
    - Guarda los archivos en una ruta definida por el usuario

 Cómo usar:
    1. Abrir un proyecto en QGIS con las capas cargadas
    2. Modificar la variable `ruta_salida` con la carpeta de destino deseada
    3. Ejecutar este script desde la consola de Python en QGIS

 Requisitos:
    - QGIS 3.x
    - Plugin 'Processing' habilitado

Autor: 95sFran (GitHub: https://github.com/95sFran)
"""

import os
import processing
from qgis.core import QgsProject

# Carpeta donde se guardarán las capas exportadas
ruta_salida = "C:/ruta/de/salida"

# Crear la carpeta si no existe
if not os.path.exists(ruta_salida):
    os.makedirs(ruta_salida)

# Obtener todas las capas cargadas en el proyecto
proyecto = QgsProject.instance()
capas = proyecto.mapLayers().values()

# Exportar cada capa como Shapefile
for capa in capas:
    nombre_capa = capa.name()
    nombre_archivo = os.path.join(ruta_salida, f"{nombre_capa}.shp")

    processing.run("native:savefeatures", {
        'INPUT': capa,
        'OUTPUT': nombre_archivo
    })

    print(f"Capa '{nombre_capa}' exportada a: {nombre_archivo}")

print("✔ Exportación completada.")
