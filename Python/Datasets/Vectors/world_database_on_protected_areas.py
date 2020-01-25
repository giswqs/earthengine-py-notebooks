# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Datasets/Vectors/world_database_on_protected_areas.py

import ee
from ee_plugin import Map

dataset = ee.FeatureCollection('WCMC/WDPA/current/polygons')
visParams = {
  'palette': ['2ed033', '5aff05', '67b9ff', '5844ff', '0a7618', '2c05ff'],
  'min': 0.0,
  'max': 1550000.0,
  'opacity': 0.8,
}
image = ee.Image().float().paint(dataset, 'REP_AREA')
Map.setCenter(41.104, -17.724, 6)
Map.addLayer(image, visParams, 'WCMC/WDPA/current/polygons')
# Map.addLayer(dataset, {}, 'for Inspector', False)


dataset = ee.FeatureCollection('WCMC/WDPA/current/points')
styleParams = {
  'color': '#4285F4',
  'width': 1,
}
protectedAreaPoints = dataset.style(**styleParams)
# Map.setCenter(110.57, 0.88, 4)
Map.addLayer(protectedAreaPoints, {}, 'WCMC/WDPA/current/points')
