#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convierte coordenadas decimales (DD) a formato DMS (grados, minutos, segundos) para todos los elementos
de la capa activa en QGIS. Se asume que la capa ya contiene los campos con coordenadas decimales (ej. 'dd_x' y 'dd_y').

Campos generados:
- latit: coordenada Y convertida a DMS
- longi: coordenada X convertida a DMS

Requisitos:
- Ejecutar dentro del entorno de QGIS.
- La capa activa debe tener los campos 'dd_x' y 'dd_y'.

Autor: 95devFran
"""

from qgis.core import QgsField, edit
from PyQt5.QtCore import QVariant
from qgis.utils import iface

# Configuración de campos
campo_dd_y = "campo de Y"    # Latitud en decimal
campo_dd_x = "campo de X"    # Longitud en decimal
campo_lat_dms = "campo de latitud"
campo_lon_dms = "campo de longitud"

# Obtener capa activa
layer = iface.activeLayer()

# Verificar si existe
if not layer or not layer.isValid():
    raise Exception(" No hay ninguna capa activa válida.")

# Añadir campos si no existen
field_names = [f.name() for f in layer.fields()]
nuevos_campos = []
if campo_lat_dms not in field_names:
    nuevos_campos.append(QgsField(campo_lat_dms, QVariant.String))
if campo_lon_dms not in field_names:
    nuevos_campos.append(QgsField(campo_lon_dms, QVariant.String))

if nuevos_campos:
    layer.dataProvider().addAttributes(nuevos_campos)
    layer.updateFields()
    print("➕ Campos añadidos.")

# Función de conversión de decimal a DMS
def convert_to_dms(dd):
    degrees = int(dd)
    abs_dd = abs(dd - degrees)
    minutes = int(abs_dd * 60)
    seconds = round((abs_dd * 60 - minutes) * 60, 2)

    if seconds >= 60:
        seconds = 0
        minutes += 1
    if minutes >= 60:
        minutes = 0
        degrees += 1

    return f"{degrees}°{minutes}'{seconds}\""

# Aplicar conversión y actualizar campos
with edit(layer):
    for feature in layer.getFeatures():
        dd_lat = feature[campo_dd_y]
        dd_lon = feature[campo_dd_x]

        if dd_lat is None or dd_lon is None:
            continue

        feature[campo_lat_dms] = convert_to_dms(dd_lat)
        feature[campo_lon_dms] = convert_to_dms(dd_lon)
        layer.updateFeature(feature)

print("✅ Conversión completada.")
