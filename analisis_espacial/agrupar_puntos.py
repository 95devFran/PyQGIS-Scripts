"""
Agrupación de puntos en QGIS basada en un campo específico y creación de puntos representativos.

Este script realiza lo siguiente:

1. Obtiene una capa de puntos cargada en el proyecto (por ejemplo, una capa de "portales").
2. Agrupa los puntos de dicha capa según los valores de un campo común (ejemplo: "direccion").
3. Para cada grupo, calcula un punto representativo que es el centroide simple (promedio de coordenadas) de los puntos agrupados.
4. Crea una nueva capa temporal de tipo punto que contiene un punto representativo por cada grupo con el valor del campo agrupador asignado.
5. Añade esta nueva capa al proyecto actual de QGIS para su visualización y uso.

Este método es útil para simplificar visualizaciones, análisis o resumen espacial agrupando múltiples puntos que comparten un mismo atributo.
"""

from qgis.core import QgsProject, QgsField, QgsFeature, QgsGeometry, QgsPointXY
from PyQt5.QtCore import QVariant

# Nombre de la capa de puntos a procesar (modificar según la capa cargada en tu proyecto)
layer_name = "portales"  # Ejemplo: capa de puntos con ubicación de portales
layer = QgsProject.instance().mapLayersByName(layer_name)[0]

# Preparar campos para la nueva capa de salida, incluyendo un campo para el agrupador (ejemplo: "direccion")
fields = layer.fields()  # Copia de los campos existentes
fields.append(QgsField("direccion", QVariant.String))  # Añadir campo para el agrupador si no está

# Crear una capa temporal de puntos para almacenar los puntos agrupados (centroides)
output_layer = QgsVectorLayer("Point?crs=EPSG:25830", "Portales Agrupados", "memory")
output_provider = output_layer.dataProvider()
output_provider.addAttributes(fields)  # Añadir campos a la capa de salida
output_layer.updateFields()

# Diccionario para almacenar listas de geometrías agrupadas por valor del campo "direccion"
grouped_points = {}

# Agrupar los puntos según el campo "direccion"
for feature in layer.getFeatures():
    direccion = feature["direccion"]
    geometry = feature.geometry()

    if direccion not in grouped_points:
        grouped_points[direccion] = []

    grouped_points[direccion].append(geometry)

# Para cada grupo, calcular el centroide simple y crear un nuevo punto representativo
for direccion, geometries in grouped_points.items():
    x_coords = [geometry.asPoint().x() for geometry in geometries]
    y_coords = [geometry.asPoint().y() for geometry in geometries]

    x_avg = sum(x_coords) / len(x_coords)
    y_avg = sum(y_coords) / len(y_coords)

    point = QgsPointXY(x_avg, y_avg)
    new_feature = QgsFeature(fields)
    new_feature.setGeometry(QgsGeometry.fromPointXY(point))
    new_feature.setAttribute("direccion", direccion)  # Asignar valor del agrupador

    output_provider.addFeature(new_feature)

# Añadir la nueva capa con puntos agrupados al proyecto QGIS
QgsProject.instance().addMapLayer(output_layer)

print("Agrupación de puntos completada.")
