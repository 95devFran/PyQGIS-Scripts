from qgis.core import (
    QgsProject, QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY, QgsField
)
from PyQt5.QtCore import QVariant

# Nombre de la capa de puntos de entrada
nombre_capa_puntos = "nombre de la capa"

# Dimensiones del rectángulo (ancho x alto) - en unidades del CRS
ancho = 4       
alto = 2.5     

# Obtener la capa de puntos por nombre
capa_puntos = QgsProject.instance().mapLayersByName(nombre_capa_puntos)

if not capa_puntos:
    print(f"No se encontró la capa '{nombre_capa_puntos}'. Verifica el nombre.")
else:
    capa_puntos = capa_puntos[0]

    # Crear una nueva capa de polígonos
    uri = "Polygon?crs=" + capa_puntos.crs().authid()
    capa_poligonos = QgsVectorLayer(uri, "rectangulos_buffer", "memory")
    prov = capa_poligonos.dataProvider()

    # Agregar campo ID
    prov.addAttributes([QgsField("ID", QVariant.Int)])
    capa_poligonos.updateFields()

    # Crear rectángulos centrados en cada punto
    nueva_entidad_id = 1
    for feature in capa_puntos.getFeatures():
        x, y = feature.geometry().asPoint().x(), feature.geometry().asPoint().y()

        # Definir los vértices del rectángulo centrado
        poligono = QgsGeometry.fromPolygonXY([[ 
            QgsPointXY(x - ancho / 2, y - alto / 2),
            QgsPointXY(x + ancho / 2, y - alto / 2),
            QgsPointXY(x + ancho / 2, y + alto / 2),
            QgsPointXY(x - ancho / 2, y + alto / 2),
            QgsPointXY(x - ancho / 2, y - alto / 2)
        ]])

        # Crear y agregar la entidad a la capa
        nueva_feature = QgsFeature()
        nueva_feature.setGeometry(poligono)
        nueva_feature.setAttributes([nueva_entidad_id])
        prov.addFeatures([nueva_feature])
        nueva_entidad_id += 1

    # Finalizar y agregar al proyecto
    capa_poligonos.updateExtents()
    QgsProject.instance().addMapLayer(capa_poligonos)
    print(f"Se generaron {nueva_entidad_id - 1} rectángulos en la capa 'rectangulos_buffer'.")
