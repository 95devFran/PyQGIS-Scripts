# -*- coding: utf-8 -*-
import os
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsVectorLayer
)

# Inicializar QGIS sin interfaz
qgis_app = QgsApplication([], False)
qgis_app.initQgis()

def añadir_capa_a_proyectos_qgis(carpeta_proyectos, ruta_capa):
    """
    Añade una capa vectorial a todos los proyectos de QGIS encontrados en una carpeta.

    :param carpeta_proyectos: Ruta a la carpeta con archivos de proyecto QGIS
    :param ruta_capa: Ruta a la capa vectorial (ej: shapefile .shp) que se va a añadir
    """
    if not os.path.isdir(carpeta_proyectos):
        print(f" Carpeta no encontrada: {carpeta_proyectos}")
        return

    if not os.path.isfile(ruta_capa):
        print(f" Capa no encontrada: {ruta_capa}")
        return

    proyectos = [
        os.path.join(carpeta_proyectos, f)
        for f in os.listdir(carpeta_proyectos)
        if f.endswith(".qgz") or f.endswith(".qgs")
    ]

    if not proyectos:
        print(" No se encontraron archivos de proyecto en la carpeta.")
        return

    print(f"Proyectos encontrados: {len(proyectos)}")

    for proyecto_path in proyectos:
        print(f"Abriendo: {proyecto_path}")
        proyecto = QgsProject.instance()
        proyecto.read(proyecto_path)

        # Cargar capa vectorial
        capa = QgsVectorLayer(ruta_capa, os.path.basename(ruta_capa), "ogr")
        if not capa.isValid():
            print(f" La capa no es válida: {ruta_capa}")
            continue

        # Añadir capa al proyecto
        proyecto.addMapLayer(capa)
        proyecto.write()  # Guarda el archivo original

        print(f"Capa añadida a: {os.path.basename(proyecto_path)}")

    print("Proceso completado con éxito.")

# --- ZONA DE CONFIGURACIÓN ---
if __name__ == "__main__":
    carpeta_proyectos = r"C:/ruta/a/carpeta_de_proyectos"
    ruta_capa = r"C:/ruta/a/la_capa.shp"
    añadir_capa_a_proyectos_qgis(carpeta_proyectos, ruta_capa)

    # Finalizar QGIS
    qgis_app.exitQgis()
