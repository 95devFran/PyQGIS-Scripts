from qgis.core import QgsProject

# Obtener capas por nombre
capa_radio = QgsProject.instance().mapLayersByName("layer2")[0]
capa_principal = QgsProject.instance().mapLayersByName("layer1")[0]

radio = 700  # metros

# Obtener el único punto
feat_punto = next(capa_radio.getFeatures())
geom_punto = feat_punto.geometry()

# Crear buffer
buffer_geom = geom_punto.buffer(radio, 20)

# Limpiar selección previa
capa_principal.removeSelection()

ids_dentro = []

for feat in capa_principal.getFeatures():
    if buffer_geom.contains(feat.geometry()):
        ids_dentro.append(feat.id())

# Seleccionar puntos dentro del radio
capa_principal.selectByIds(ids_dentro)

print(f"{len(ids_dentro)} elementos encontrados en un radio de {radio} metros.")
