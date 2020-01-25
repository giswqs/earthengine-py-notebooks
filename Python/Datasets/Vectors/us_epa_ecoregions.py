# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Datasets/Vectors/us_epa_ecoregions.py

import ee 
from ee_plugin import Map 

dataset = ee.FeatureCollection('EPA/Ecoregions/2013/L3')
visParams = {
  'palette': ['0a3b04', '1a9924', '15d812'],
  'min': 23.0,
  'max': 3.57e+11,
  'opacity': 0.8,
}
image = ee.Image().float().paint(dataset, 'shape_area')
Map.setCenter(-99.814, 40.166, 5)
Map.addLayer(image, visParams, 'EPA/Ecoregions/2013/L3')
# Map.addLayer(dataset, {}, 'for Inspector', False)


dataset = ee.FeatureCollection('EPA/Ecoregions/2013/L4')
visParams = {
  'palette': ['0a3b04', '1a9924', '15d812'],
  'min': 0.0,
  'max': 67800000000.0,
  'opacity': 0.8,
}
image = ee.Image().float().paint(dataset, 'shape_area')
Map.setCenter(-99.814, 40.166, 5)
Map.addLayer(image, visParams, 'EPA/Ecoregions/2013/L4')
# Map.addLayer(dataset, {}, 'for Inspector', False)
