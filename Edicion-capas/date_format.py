from datetime import datetime
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterField,
    QgsField,
    edit
)
from PyQt5.QtCore import QVariant

class ConvertirEpochAFecha(QgsProcessingAlgorithm):
    INPUT       = 'INPUT'
    CAMPO_EPOCH = 'CAMPO_EPOCH'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(self.INPUT, 'Capa')
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.CAMPO_EPOCH,
                'Campo con la fecha a cambiar formato',
                parentLayerParameterName=self.INPUT
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        capa        = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        campo_epoch = self.parameterAsString(parameters, self.CAMPO_EPOCH, context)
        idx         = capa.fields().indexOf(campo_epoch)
        total       = capa.featureCount()

        with edit(capa):
            for i, feature in enumerate(capa.getFeatures()):
                if feedback.isCanceled():
                    break
                feedback.setProgress(int(i / total * 100))

                try:
                    valor = feature[campo_epoch]

                    # Intenta primero como epoch numérico
                    try:
                        dt = datetime.fromtimestamp(float(valor))
                    except:
                        # Si falla, intenta parsear el texto que ya hay
                        dt = datetime.strptime(str(valor), '%Y-%m-%d %H:%M:%S')

                    fecha_str = dt.strftime('%d/%m/%Y %H:%M:%S')
                    capa.changeAttributeValue(feature.id(), idx, fecha_str)
                except:
                    pass  # NULL, vacío o cualquier error → lo salta

        feedback.pushInfo("¡Proceso completado!")
        return {}

    def name(self):           return 'convertir_epoch_a_fecha'
    def displayName(self):    return 'Formato fecha correcto'
    def group(self):          return 'Mis scripts'
    def groupId(self):        return 'mis_scripts'
    def createInstance(self): return ConvertirEpochAFecha()
    def tr(self, string):     return string
