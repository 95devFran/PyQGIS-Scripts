#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exporta campos específicos de una capa cargada en QGIS a un archivo CSV.

Este script toma como entrada:
- El nombre de una capa cargada en el proyecto.
- Una lista de campos deseados a exportar.
- La ruta de salida del archivo CSV.

Requisitos:
- Ejecutar dentro del entorno de QGIS (PyQGIS).
- La capa debe estar previamente cargada en el proyecto.

Autor: 95devFran 
"""

import os
import csv
from qgis.core import QgsProject

# === Configuración ===
nombre_capa = "capa deseada"  # Nombre exacto de la capa cargada en QGIS
campos_deseados = ["campo 1, campo2"]  # Lista de campos a exportar
ruta_salida = "ruta/salida/deseada.csv"  # Ruta donde se guardará el CSV

# === Obtener la capa ===
capas = QgsProject.instance().mapLayersByName(nombre_capa)
if not capas:
    raise Exception(f" No se encontró ninguna capa con el nombre '{nombre_capa}'")

capa = capas[0]
print(f" Capa '{nombre_capa}' cargada con {capa.featureCount()} entidades.")

# === Validación de campos ===
campos_disponibles = [f.name() for f in capa.fields()]
campos_exportables = [campo for campo in campos_deseados if campo in campos_disponibles]

if not campos_exportables:
    raise Exception(" Ninguno de los campos especificados se encuentra en la capa.")

print(f" Campos a exportar: {campos_exportables}")

# === Escritura del archivo CSV ===
with open(ruta_salida, mode="w", newline="", encoding="utf-8-sig") as archivo_csv:
    writer = csv.writer(archivo_csv)
    writer.writerow(campos_exportables)  # Cabecera

    total = 0
    for feature in capa.getFeatures():
        fila = [feature[campo] for campo in campos_exportables]
        writer.writerow(fila)
        total += 1

print(f" Exportación completa: {total} filas guardadas en '{ruta_salida}'")

# === Abrir el archivo exportado (opcional) ===
os.startfile(ruta_salida)
