"""
 Script PyQGIS: Generación de buffers cuadrados desde una capa de puntos

 ¿Qué hace?
    - A partir de una capa de puntos, genera cuadrados centrados en cada punto
    - Cada cuadrado tiene el área o tamaño definido por el usuario
    - Los cuadrados se agregan como una nueva capa de polígonos en el proyecto QGIS

 Uso:
    1. Abrir un proyecto en QGIS con una capa de puntos cargada
    2. Cambiar el valor de `nombre_capa_puntos` al nombre exacto de la capa
    3. Ajustar el valor de `lado` según el área deseada (en unidades del CRS)
    4. Ejecutar el script en la consola de Python de QGIS

 Requisitos:
    - QGIS 3.x
    - Capa de entrada con geometría de tipo Punto

Autor: 95devFran (https://github.com/95devFran)
"""

from qgis.core import (
    QgsProject, QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY, QgsField
)
from PyQt5.QtCore import QVariant
import math

#  Nombre de la capa de puntos sobre la que vas a crear el buffer
nombre_capa_puntos = "nombre de capa de puntos"

#  Lado del cuadrado (en unidades del CRS, por ejemplo, metros si el CRS es proyectado)
lado = math.sqrt(199.9480)  # Aproximadamente 14.14 m para un área de 199.9480 m²

#  Buscar la capa en el proyecto actual
capa_puntos = QgsProject.instance().mapLayersByName(nombre_capa_puntos)

if not capa_puntos:
    print(f"No se encontró ninguna capa llamada '{nombre_capa_puntos}'. Verifica el nombre.")
else:
    capa_puntos = capa_puntos[0]  # Selecciona la primera coincidencia

    #  Crear una nueva capa vectorial de polígonos en memoria, con el mismo CRS
    uri = "Polygon?crs=" + capa_puntos.crs().authid()
    capa_poligonos = QgsVectorLayer(uri, "cuadrados_buffer", "memory")
    prov = capa_poligonos.dataProvider()

    #  Agregar campo ID a la capa de salida
    prov.addAttributes([QgsField("ID", QVariant.Int)])
    capa_poligonos.updateFields()

    #  Crear un cuadrado centrado en cada punto
    nueva_entidad_id = 1
    for feature in capa_puntos.getFeatures():
        x, y = feature.geometry().asPoint().x(), feature.geometry().asPoint().y()

        # Definir las coordenadas de los vértices del cuadrado
        poligono = QgsGeometry.fromPolygonXY([[
            QgsPointXY(x - lado / 2, y - lado / 2),
            QgsPointXY(x + lado / 2, y - lado / 2),
            QgsPointXY(x + lado / 2, y + lado / 2),
            QgsPointXY(x - lado / 2, y + lado / 2),
            QgsPointXY(x - lado / 2, y - lado / 2)
        ]])

        # Crear la nueva entidad poligonal y asignar atributos
        nueva_feature = QgsFeature()
        nueva_feature.setGeometry(poligono)
        nueva_feature.setAttributes([nueva_entidad_id])
        prov.addFeatures([nueva_feature])
        nueva_entidad_id += 1

    #  Actualizar la capa y añadirla al proyecto
    capa_poligonos.updateExtents()
    QgsProject.instance().addMapLayer(capa_poligonos)

    print(f" Se generaron {nueva_entidad_id - 1} polígonos cuadrados como buffer.")
