"""
--------------------------------------------------------------

Este script añade un nuevo campo a una capa vectorial en formato SHP
y luego asigna valores a ese campo para cada entidad según una lógica
personalizable (por ejemplo, a partir de un diccionario o datos externos).

Funcionalidades:
- Verifica que la capa exista y sea válida.
- Añade un campo nuevo con el nombre, tipo y longitud definidos.
- Actualiza la capa con el nuevo campo.
- Recorre las entidades y asigna valores personalizados a ese campo.
- Guarda los cambios realizados en la capa.

Requisitos:
- Ejecutar en entorno QGIS con PyQGIS.
- Ruta válida a un archivo SHP.

--------------------------------------------------------------
"""

from qgis.core import (
    QgsVectorLayer,
    QgsField,
    edit
)
from PyQt5.QtCore import QVariant
import os

# --- CONFIGURACIÓN ---

shapefile_path = r"RUTA/A/TU/CAPA.shp"  # Ruta al archivo shapefile
new_field_name = "NUEVO_CAMPO"           # Nombre del campo a crear
new_field_type = QVariant.String         # Tipo del campo (ejemplo: String)
new_field_length = 20                    # Longitud del campo (para campos string)

# Diccionario ejemplo para asignar valores al campo nuevo:
# Clave: ID o atributo único de la entidad (por ejemplo, 'id' o 'nombre')
# Valor: valor a asignar en el nuevo campo
values_dict = {
    "entidad_1": "valor_1",
    "entidad_2": "valor_2",
    # ...
}

# --- FIN DE CONFIGURACIÓN ---


if not os.path.exists(shapefile_path):
    print(f"No se encontró el archivo shapefile: {shapefile_path}")
else:
    # Cargar la capa
    layer = QgsVectorLayer(shapefile_path, "CapaBase", "ogr")

    if not layer.isValid():
        print("Error al cargar la capa vectorial.")
    else:
        # Añadir nuevo campo si no existe
        existing_fields = [field.name() for field in layer.fields()]
        if new_field_name not in existing_fields:
            layer.startEditing()
            new_field = QgsField(new_field_name, new_field_type, len=new_field_length)
            layer.dataProvider().addAttributes([new_field])
            layer.updateFields()
            layer.commitChanges()
            print(f"Campo '{new_field_name}' añadido correctamente.")
        else:
            print(f"El campo '{new_field_name}' ya existe en la capa.")

        # Actualizar la capa para reflejar el nuevo campo
        layer = QgsVectorLayer(shapefile_path, "CapaBase", "ogr")

        # Asignar valores al nuevo campo según values_dict
        field_idx = layer.fields().indexFromName(new_field_name)
        if field_idx == -1:
            print(f"No se encontró el campo '{new_field_name}' para asignar valores.")
        else:
            with edit(layer):
                for feature in layer.getFeatures():
                    # Aquí se debe definir la clave para buscar en values_dict,
                    # por ejemplo un campo identificador único:
                    key = feature["id"] if "id" in layer.fields().names() else None
                    if key and key in values_dict:
                        layer.changeAttributeValue(feature.id(), field_idx, values_dict[key])
            print(f"Valores asignados correctamente al campo '{new_field_name}'.")
