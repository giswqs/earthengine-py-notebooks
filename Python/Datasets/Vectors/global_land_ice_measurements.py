# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Datasets/Vectors/global_land_ice_measurements.py

import ee 
from ee_plugin import Map 

dataset = ee.FeatureCollection('GLIMS/current')
visParams = {
  'palette': ['gray', 'cyan', 'blue'],
  'min': 0.0,
  'max': 10.0,
  'opacity': 0.8,
}

image = ee.Image().float().paint(dataset, 'area')
Map.setCenter(-35.618, 66.743, 7)
Map.addLayer(image, visParams, 'GLIMS/current')
# Map.addLayer(dataset, {}, 'for Inspector', False)
