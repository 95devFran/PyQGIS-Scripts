layer = iface.activeLayer()

crs_src = layer.crs()
crs_dest = QgsCoordinateReferenceSystem("EPSG:4326")

transform = QgsCoordinateTransform(crs_src, crs_dest, QgsProject.instance())

with edit(layer):
    for feat in layer.getFeatures():
        geom = feat.geometry()

        #obtener centroide
        centroid = geom.entroid().asPoint()

        point_wgs = transform.transform(centroid)

        feat["long"] = round(point_wgs.x(), 3)
        feat["lat"] = round(point_wgs.y(), 3)

        layer.updateFeature(feat)

print("ok")
