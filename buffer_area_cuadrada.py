from qgis.core import (
    QgsProject, QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY, QgsField
)
from PyQt5.QtCore import QVariant
import math

# Nombre para la capa de puntos a procesar
nombre_capa_puntos = "nombre de capa de puntos"

# Dimensión del lado del cuadrado (en unidades del CRS)
lado = math.sqrt(199.9480)  # Ajusta este valor según el área deseada (ej. ~1.5 metros de lado)

# Obtener la capa de puntos por nombre
capa_puntos = QgsProject.instance().mapLayersByName(nombre_capa_puntos)

if not capa_puntos:
    print(f"No se encontró ninguna capa llamada '{nombre_capa_puntos}'. Verifica el nombre e inténtalo de nuevo.")
else:
    capa_puntos = capa_puntos[0]

    # Crear una nueva capa de polígonos con el mismo CRS que la capa de puntos
    uri = "Polygon?crs=" + capa_puntos.crs().authid()
    capa_poligonos = QgsVectorLayer(uri, "cuadrados_buffer", "memory")
    prov = capa_poligonos.dataProvider()

    # Añadir campo ID a la nueva capa
    prov.addAttributes([QgsField("ID", QVariant.Int)])
    capa_poligonos.updateFields()

    # Crear cuadrados centrados en cada punto
    nueva_entidad_id = 1
    for feature in capa_puntos.getFeatures():
        x, y = feature.geometry().asPoint().x(), feature.geometry().asPoint().y()

        # Definir los vértices del cuadrado alrededor del punto
        poligono = QgsGeometry.fromPolygonXY([[
            QgsPointXY(x - lado / 2, y - lado / 2),
            QgsPointXY(x + lado / 2, y - lado / 2),
            QgsPointXY(x + lado / 2, y + lado / 2),
            QgsPointXY(x - lado / 2, y + lado / 2),
            QgsPointXY(x - lado / 2, y - lado / 2)
        ]])

        # Crear y agregar el nuevo polígono
        nueva_feature = QgsFeature()
        nueva_feature.setGeometry(poligono)
        nueva_feature.setAttributes([nueva_entidad_id])
        prov.addFeatures([nueva_feature])
        nueva_entidad_id += 1

    # Actualizar la extensión de la capa y agregarla al proyecto
    capa_poligonos.updateExtents()
    QgsProject.instance().addMapLayer(capa_poligonos)

    print(f"Se generaron {nueva_entidad_id - 1} polígonos cuadrados como buffer.")
