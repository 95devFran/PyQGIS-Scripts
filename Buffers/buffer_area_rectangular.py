"""
 Script PyQGIS: Generación de rectángulos centrados desde puntos

 ¿Qué hace?
    - A partir de una capa de puntos, genera rectángulos centrados en cada punto.
    - Cada rectángulo tiene dimensiones fijas (ancho x alto) definidas por el usuario.
    - Se crea una nueva capa de polígonos en memoria y se añade al proyecto.

 Uso:
    1. Abre un proyecto de QGIS con una capa de puntos cargada.
    2. Modifica el valor de `nombre_capa_puntos` por el nombre exacto de la capa.
    3. Ajusta los valores de `ancho` y `alto` según tus necesidades (en unidades del CRS).
    4. Ejecuta el script en la consola de Python de QGIS.

 Requisitos:
    - QGIS 3.x
    - La capa de entrada debe contener geometrías de tipo Punto

Autor: 95devFran (https://github.com/95devFran)
"""

from qgis.core import (
    QgsProject, QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY, QgsField
)
from PyQt5.QtCore import QVariant

#  Nombre de la capa de puntos sobre la que se crea el buffer
nombre_capa_puntos = "nombre de la capa"

#  Dimensiones del rectángulo (en unidades del CRS, p. ej., metros)
ancho = 4       # Ej. 4 metros de ancho
alto = 2.5      # Ej. 2.5 metros de alto

#  Buscar la capa de puntos en el proyecto
capa_puntos = QgsProject.instance().mapLayersByName(nombre_capa_puntos)

if not capa_puntos:
    print(f"❌ No se encontró la capa '{nombre_capa_puntos}'. Verifica el nombre.")
else:
    capa_puntos = capa_puntos[0]

    #  Crear una nueva capa de polígonos en memoria con el mismo CRS
    uri = "Polygon?crs=" + capa_puntos.crs().authid()
    capa_poligonos = QgsVectorLayer(uri, "rectangulos_buffer", "memory")
    prov = capa_poligonos.dataProvider()

    #  Agregar un campo ID a la capa de salida
    prov.addAttributes([QgsField("ID", QVariant.Int)])
    capa_poligonos.updateFields()

    #  Crear rectángulos centrados en cada punto de entrada
    nueva_entidad_id = 1
    for feature in capa_puntos.getFeatures():
        x, y = feature.geometry().asPoint().x(), feature.geometry().asPoint().y()

        # Definir los vértices del rectángulo
        poligono = QgsGeometry.fromPolygonXY([[ 
            QgsPointXY(x - ancho / 2, y - alto / 2),
            QgsPointXY(x + ancho / 2, y - alto / 2),
            QgsPointXY(x + ancho / 2, y + alto / 2),
            QgsPointXY(x - ancho / 2, y + alto / 2),
            QgsPointXY(x - ancho / 2, y - alto / 2)  # Cierre del polígono
        ]])

        # Crear la nueva entidad y agregarla a la capa
        nueva_feature = QgsFeature()
        nueva_feature.setGeometry(poligono)
        nueva_feature.setAttributes([nueva_entidad_id])
        prov.addFeatures([nueva_feature])
        nueva_entidad_id += 1

    #  Actualizar la capa y agregarla al proyecto
    capa_poligonos.updateExtents()
    QgsProject.instance().addMapLayer(capa_poligonos)

    print(f" Se generaron {nueva_entidad_id - 1} rectángulos en la capa 'rectangulos_buffer'.")
