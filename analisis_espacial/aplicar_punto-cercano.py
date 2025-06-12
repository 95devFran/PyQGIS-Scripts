"""
Actualización de atributos en una capa vectorial basada en la proximidad a otra capa en QGIS.

Este script realiza los siguientes pasos:

1. Obtiene dos capas cargadas en el proyecto QGIS:
   - Una capa principal en la que se va a actualizar un campo (ejemplo: capa de redes o líneas).
   - Una capa secundaria que contiene puntos o etiquetas (ejemplo: textos o nombres concretos de posiciones determinadas).

2. Verifica si el campo destino existe en la capa principal; si no, lo crea.

3. Para cada entidad de la capa principal, calcula cuál es la entidad más cercana en la capa secundaria basándose en la distancia geométrica.

4. Extrae un valor de atributo de la entidad más cercana (por ejemplo, un texto descriptivo) y lo asigna al campo de la capa principal para esa entidad.

5. Guarda los cambios realizados en la capa principal.

Este método es útil para asignar atributos basados en la cercanía espacial entre dos capas, como etiquetar líneas con el nombre 
del punto más cercano o asociar atributos de puntos vecinos.
"""

from qgis.core import QgsProject, QgsField
from PyQt5.QtCore import QVariant

# Obtener las capas por nombre (modificar por los nombres que existan en tu proyecto)
capa_principal = QgsProject.instance().mapLayersByName("CAPA_PRINCIPAL")[0]
capa_secundaria = QgsProject.instance().mapLayersByName("CAPA_SECUNDARIA")[0]

if not capa_principal or not capa_secundaria:
    print("No se encontraron las capas necesarias.")
else:
    print("Capas cargadas correctamente.")

    # Verificar si el campo destino existe, si no, crearlo
    if "campo_destino" not in [field.name() for field in capa_principal.fields()]:
        capa_principal.dataProvider().addAttributes([QgsField("campo_destino", QVariant.String)])
        capa_principal.updateFields()
        print("Campo 'campo_destino' agregado a la capa principal.")

    # Iniciar edición en la capa principal
    capa_principal.startEditing()

    # Iterar por cada entidad de la capa principal
    for entidad_principal in capa_principal.getFeatures():
        geom_principal = entidad_principal.geometry()
        valor_cercano = None
        distancia_minima = float("inf")

        # Buscar la entidad más cercana en la capa secundaria
        for entidad_secundaria in capa_secundaria.getFeatures():
            geom_secundaria = entidad_secundaria.geometry()
            distancia = geom_principal.distance(geom_secundaria)

            if distancia < distancia_minima:
                distancia_minima = distancia
                valor_cercano = entidad_secundaria["CAMPO_ORIGEN"]

        # Asignar el valor más cercano al campo destino
        if valor_cercano:
            entidad_principal["campo_destino"] = valor_cercano
            capa_principal.updateFeature(entidad_principal)

    # Guardar los cambios
    if capa_principal.commitChanges():
        print("Campo 'campo_destino' actualizado con éxito.")
    else:
        print("Error al guardar los cambios.")
