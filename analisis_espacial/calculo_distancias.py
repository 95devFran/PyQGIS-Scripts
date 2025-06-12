#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Calcular la distancia entre entidades con el mismo identificador entre dos capas cargadas en QGIS.

Este script busca entidades que compartan un valor común en un campo de identificación,
compara su geometría y guarda la distancia mínima encontrada en un campo de la primera capa.

Uso:
- Asegúrate de tener dos capas vectoriales cargadas en QGIS.
- El campo común debe estar presente en ambas capas.
- Se añadirá automáticamente un nuevo campo en la capa origen si no existe.

Requisitos:
- Ejecutar desde el entorno de QGIS 

Autor: 95devFra
"""

from qgis.core import QgsProject, QgsField, edit
from PyQt5.QtCore import QVariant

# Parámetros configurables
nombre_capa_origen = "capa origen"
nombre_capa_destino = "capa destino"
campo_identificador = "campo que comparten ambas capas"
campo_distancia = "campo nuevo para ver la distancia"

# Obtener capas
capa_origen = QgsProject.instance().mapLayersByName(nombre_capa_origen)
capa_destino = QgsProject.instance().mapLayersByName(nombre_capa_destino)

if not capa_origen or not capa_destino:
    print("No se encontraron una o ambas capas. Verifica los nombres.")
    raise ValueError("Capas no encontradas.")

capa_origen = capa_origen[0]
capa_destino = capa_destino[0]

# Verificación de validez
if not capa_origen.isValid() or not capa_destino.isValid():
    print(" Una o ambas capas no son válidas.")
else:
    # Añadir campo si no existe
    if campo_distancia not in capa_origen.fields().names():
        capa_origen.dataProvider().addAttributes([QgsField(campo_distancia, QVariant.Double)])
        capa_origen.updateFields()
        print(f"➕ Campo '{campo_distancia}' añadido.")

    with edit(capa_origen):
        for f_origen in capa_origen.getFeatures():
            id_origen = f_origen[campo_identificador]
            geom_origen = f_origen.geometry()

            min_dist = float("inf")
            found = False

            for f_destino in capa_destino.getFeatures():
                if f_destino[campo_identificador] == id_origen:
                    geom_destino = f_destino.geometry()
                    dist = geom_origen.distance(geom_destino)
                    if dist < min_dist:
                        min_dist = dist
                        found = True

            if found:
                capa_origen.changeAttributeValue(
                    f_origen.id(),
                    capa_origen.fields().indexOf(campo_distancia),
                    min_dist
                )
                print(f"✔ Distancia actualizada para ID {id_origen}: {min_dist}")
            else:
                print(f"⚠ No se encontró coincidencia para ID: {id_origen}")

    print("✅ Proceso completado correctamente.")
