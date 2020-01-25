import ee
from ee_plugin import Map
dataset = ee.Image('JRC/GSW1_1/GlobalSurfaceWater')
occurrence = dataset.select('occurrence');
occurrenceVis = {'min': 0.0, 'max': 100.0, 'palette': ['ffffff', 'ffbbbb', '0000ff']}
Map.setCenter(59.414, 45.182, 6)
Map.addLayer(occurrence, occurrenceVis, 'Occurrence')