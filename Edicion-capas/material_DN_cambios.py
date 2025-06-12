from qgis.core import (
    QgsProject,
    QgsField,
    QgsExpression,
    QgsVectorLayer,
    QgsFeature,
    QgsVectorDataProvider
)
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox

class EditLayerDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor de materiales y DN")
        self.setGeometry(300, 300, 400, 200)
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Selección de capa
        self.layer_label = QLabel("Qué capa quieres editar:")
        self.layer_combo = QComboBox()
        layers = QgsProject.instance().mapLayers().values()
        self.layer_combo.addItems([layer.name() for layer in layers])
        
        layout.addWidget(self.layer_label)
        layout.addWidget(self.layer_combo)
        
        # Campo material
        self.material_label = QLabel("Introduce el 'material':")
        self.material_input = QLineEdit()
        layout.addWidget(self.material_label)
        layout.addWidget(self.material_input)
        
        # Campo DN
        self.dn_label = QLabel("Introduce el 'DN':")
        self.dn_input = QLineEdit()
        layout.addWidget(self.dn_label)
        layout.addWidget(self.dn_input)
        
        # Botón de ejecutar
        self.run_button = QPushButton("Ejecutar")
        self.run_button.clicked.connect(self.run_script)
        layout.addWidget(self.run_button)
        
        # Configurar layout
        self.setLayout(layout)
    
    def run_script(self):
        # Obtener valores ingresados
        layer_name = self.layer_combo.currentText()
        material_value = self.material_input.text()
        try:
            dn_value = int(self.dn_input.text())
        except ValueError:
            QMessageBox.critical(self, "Error", "El valor de 'DN' debe ser un número entero.")
            return
        
        # Obtener la capa seleccionada
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        if not layer:
            QMessageBox.critical(self, "Error", f"No se encontró la capa {layer_name}.")
            return
        
        # Comenzar una edición en la capa
        if not layer.isEditable():
            layer.startEditing()
        
        # Verificar si los campos ya existen
        field_names = [field.name() for field in layer.fields()]
        changes = False

        if "material" not in field_names:
            layer.dataProvider().addAttributes([QgsField("material", QVariant.String)])
            changes = True

        if "DN" not in field_names:
            layer.dataProvider().addAttributes([QgsField("DN", QVariant.Int)])
            changes = True

        if changes:
            layer.updateFields()  # Actualizar la estructura de campos
            QMessageBox.information(self, "Campos creados", "Se crearon los campos 'material' y 'DN'.")
        
        # Asignar valores a las entidades
        for feature in layer.getFeatures():
            feature["material"] = material_value
            feature["DN"] = dn_value
            layer.updateFeature(feature)
        
        # Guardar cambios
        if layer.commitChanges():
            QMessageBox.information(self, "Éxito", "¡HECHO!")
        else:
            QMessageBox.critical(self, "Error", "Error al guardar los cambios en la capa.")

# Mostrar el diálogo sin crear una nueva instancia de QApplication
dialog = EditLayerDialog()
dialog.exec_()
