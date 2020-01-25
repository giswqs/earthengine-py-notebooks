# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Datasets/Vectors/us_census_blocks.py

import ee 
from ee_plugin import Map 

dataset = ee.FeatureCollection('TIGER/2010/Blocks')
visParams = {
  'min': 0.0,
  'max': 700.0,
  'palette': ['black', 'brown', 'yellow', 'orange', 'red']
}

# Turn the strings into numbers
dataset = dataset.map(lambda f: f.set('pop10', ee.Number.parse(f.get('pop10'))))

image = ee.Image().float().paint(dataset, 'pop10')

Map.setCenter(-73.99172, 40.74101, 13)
Map.addLayer(image, visParams, 'TIGER/2010/Blocks')
# Map.addLayer(dataset, {}, 'for Inspector', False)
