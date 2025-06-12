"""
Editor de campos en capas de QGIS mediante interfaz gráfica.

Este script abre una ventana en QGIS donde puedes:
1. Seleccionar una capa cargada en el proyecto.
2. Cargar y seleccionar uno de sus campos existentes para editar.
3. Introducir un valor que se asignará a todas las entidades de la capa en ese campo.
4. Si el campo seleccionado no existe, te preguntará si deseas crearlo (como campo texto).
5. Aplicar los cambios sin cerrar la ventana, permitiendo editar otros campos o valores de forma iterativa.

El proceso es:
- Seleccionas la capa.
- Presiona "Cargar campos" para listar los campos de la capa.
- Selecciona un campo a modificar.
- Escribe el valor que deseas asignar.
- Presiona en "Aplicar valor a todas las entidades".
- El campo se actualiza con ese valor para todas las entidades.
- Puedes repetir la operación para otros campos o valores sin cerrar la ventana.

Esta herramienta facilita la edición rápida de varios campos en capas vectoriales dentro de QGIS.
"""

from qgis.core import (
    QgsProject,
    QgsField,
    QgsVectorLayer
)
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox
)

class EditLayerDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor de campos en capa")
        self.setGeometry(300, 300, 400, 200)
        
        layout = QVBoxLayout()
        
        # Selección de capa
        self.layer_label = QLabel("Selecciona la capa a editar:")
        self.layer_combo = QComboBox()
        layers = QgsProject.instance().mapLayers().values()
        self.layer_combo.addItems([layer.name() for layer in layers])
        layout.addWidget(self.layer_label)
        layout.addWidget(self.layer_combo)
        
        # Botón para cargar campos de la capa seleccionada
        self.load_fields_button = QPushButton("Cargar campos de la capa")
        self.load_fields_button.clicked.connect(self.load_fields)
        layout.addWidget(self.load_fields_button)
        
        # Selección de campo
        self.field_label = QLabel("Selecciona el campo a modificar:")
        self.field_combo = QComboBox()
        layout.addWidget(self.field_label)
        layout.addWidget(self.field_combo)
        
        # Entrada de valor
        self.value_label = QLabel("Introduce el valor a asignar:")
        self.value_input = QLineEdit()
        layout.addWidget(self.value_label)
        layout.addWidget(self.value_input)
        
        # Botón para aplicar cambios
        self.apply_button = QPushButton("Aplicar valor a todas las entidades")
        self.apply_button.clicked.connect(self.apply_value)
        layout.addWidget(self.apply_button)
        
        self.setLayout(layout)
    
    def load_fields(self):
        # Limpiar el combo de campos
        self.field_combo.clear()
        
        layer_name = self.layer_combo.currentText()
        layer_list = QgsProject.instance().mapLayersByName(layer_name)
        if not layer_list:
            QMessageBox.critical(self, "Error", f"No se encontró la capa {layer_name}.")
            return
        layer = layer_list[0]
        
        # Obtener campos de la capa
        fields = layer.fields()
        field_names = [field.name() for field in fields]
        self.field_combo.addItems(field_names)
    
    def apply_value(self):
        layer_name = self.layer_combo.currentText()
        field_name = self.field_combo.currentText()
        value = self.value_input.text()
        
        if not field_name:
            QMessageBox.warning(self, "Atención", "Selecciona un campo primero.")
            return
        
        layer_list = QgsProject.instance().mapLayersByName(layer_name)
        if not layer_list:
            QMessageBox.critical(self, "Error", f"No se encontró la capa {layer_name}.")
            return
        
        layer = layer_list[0]
        
        # Si el campo no existe en la capa, preguntar si quiere crearlo
        if field_name not in [f.name() for f in layer.fields()]:
            res = QMessageBox.question(
                self,
                "Campo no existe",
                f"El campo '{field_name}' no existe en la capa. ¿Quieres crearlo como texto?",
                QMessageBox.Yes | QMessageBox.No
            )
            if res == QMessageBox.Yes:
                layer.startEditing()
                new_field = QgsField(field_name, QVariant.String)
                layer.dataProvider().addAttributes([new_field])
                layer.updateFields()
                layer.commitChanges()
                QMessageBox.information(self, "Campo creado", f"Campo '{field_name}' creado correctamente.")
            else:
                return
        
        # Asignar valor a todas las entidades en modo edición
        if not layer.isEditable():
            layer.startEditing()
        
        field_idx = layer.fields().indexFromName(field_name)
        
        with edit(layer):
            for feature in layer.getFeatures():
                # Intentar convertir valor si campo es numérico
                field_type = layer.fields().field(field_idx).type()
                if field_type in [QVariant.Int, QVariant.Double]:
                    try:
                        if field_type == QVariant.Int:
                            val = int(value)
                        else:
                            val = float(value)
                    except ValueError:
                        QMessageBox.warning(self, "Error", f"El valor para '{field_name}' debe ser numérico.")
                        return
                else:
                    val = value
                
                layer.changeAttributeValue(feature.id(), field_idx, val)
        
        # Guardar cambios
        if layer.commitChanges():
            QMessageBox.information(self, "Éxito", f"Valor '{value}' asignado a todas las entidades en '{field_name}'.")
            # Limpiar el input para facilitar nueva edición
            self.value_input.clear()
        else:
            QMessageBox.critical(self, "Error", "No se pudieron guardar los cambios.")

# Ejecutar el diálogo
dialog = EditLayerDialog()
dialog.exec_()
