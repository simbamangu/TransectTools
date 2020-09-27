"""
Model exported as python.
Name : Grid Stratum to Transects
Group : Survey Tools
With QGIS : 31415
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterString
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterFeatureSource
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsExpression
import processing


class GridStratumToTransects(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterString('centrerotn', 'centreRotn', multiLine=False, defaultValue=''))
        self.addParameter(QgsProcessingParameterVectorLayer('grid', 'Grid', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('rotation', 'rotation', type=QgsProcessingParameterNumber.Double, minValue=0, maxValue=360, defaultValue=0))
        self.addParameter(QgsProcessingParameterNumber('spacing', 'spacing', type=QgsProcessingParameterNumber.Double, minValue=0, maxValue=100000, defaultValue=5000))
        self.addParameter(QgsProcessingParameterFeatureSource('stratumselection', 'stratumSelection', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Transects', 'Transects', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(3, model_feedback)
        results = {}
        outputs = {}

        # Translate
        alg_params = {
            'DELTA_M': 0,
            'DELTA_X': QgsExpression('rand(0,  @spacing )').evaluate(),
            'DELTA_Y': QgsExpression('rand(0,  @spacing )').evaluate(),
            'DELTA_Z': 0,
            'INPUT': parameters['grid'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Translate'] = processing.run('native:translategeometry', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Rotate
        alg_params = {
            'ANCHOR': parameters['centrerotn'],
            'ANGLE': parameters['rotation'],
            'INPUT': outputs['Translate']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Rotate'] = processing.run('native:rotatefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Clip
        alg_params = {
            'INPUT': outputs['Rotate']['OUTPUT'],
            'OVERLAY': parameters['stratumselection'],
            'OUTPUT': parameters['Transects']
        }
        outputs['Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Transects'] = outputs['Clip']['OUTPUT']
        return results

    def name(self):
        return 'Grid Stratum to Transects'

    def displayName(self):
        return 'Grid Stratum to Transects'

    def group(self):
        return 'Survey Tools'

    def groupId(self):
        return 'Survey Tools'

    def createInstance(self):
        return GridStratumToTransects()
