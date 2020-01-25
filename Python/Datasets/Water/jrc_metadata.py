import ee 
from ee_plugin import Map 

dataset = ee.Image('JRC/GSW1_1/Metadata')
detectionsObservations = dataset.select(['detections', 'valid_obs', 'total_obs'])
visParams = {
  'min': 100.0,
  'max': 900.0,
}
Map.setCenter(4.72, -2.48, 2)
Map.addLayer(detectionsObservations, visParams, 'Detections/Observations')
