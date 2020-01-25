# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Datasets/Vectors/us_census_datasets.py

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


dataset = ee.FeatureCollection('TIGER/2010/Tracts_DP1')
visParams = {
  'min': 0,
  'max': 4000,
  'opacity': 0.8,
}

# Turn the strings into numbers
dataset = dataset.map(lambda f: f.set('shape_area', ee.Number.parse(f.get('dp0010001'))))

# Map.setCenter(-103.882, 43.036, 8)
image = ee.Image().float().paint(dataset, 'dp0010001')

Map.addLayer(image, visParams, 'TIGER/2010/Tracts_DP1')
# Map.addLayer(dataset, {}, 'for Inspector', False)


dataset = ee.FeatureCollection('TIGER/2010/ZCTA5')
visParams = {
  'palette': ['black', 'purple', 'blue', 'green', 'yellow', 'orange', 'red'],
  'min': 500000,
  'max': 1000000000,
}

zctaOutlines = ee.Image().float().paint(**{
  'featureCollection': dataset,
  'color': 'black',
  'width': 1
})

image = ee.Image().float().paint(dataset, 'ALAND10')
# Map.setCenter(-93.8008, 40.7177, 6)
Map.addLayer(image, visParams, 'TIGER/2010/ZCTA5')
Map.addLayer(zctaOutlines, {}, 'borders')
# Map.addLayer(dataset, {}, 'for Inspector', False)


dataset = ee.FeatureCollection('TIGER/2016/Roads')
roads = dataset.style(**{'color': '#4285F4', 'width': 1})
Map.setCenter(-73.99172, 40.74101, 12)
Map.addLayer(roads, {}, 'TIGER/2016/Roads')


dataset = ee.FeatureCollection('TIGER/2018/Counties')
visParams = {
  'palette': ['purple', 'blue', 'green', 'yellow', 'orange', 'red'],
  'min': 0,
  'max': 50,
  'opacity': 0.8,
}

# Turn the strings into numbers
dataset = dataset.map(lambda f: f.set('STATEFP', ee.Number.parse(f.get('STATEFP'))))

image = ee.Image().float().paint(dataset, 'STATEFP')
countyOutlines = ee.Image().float().paint(**{
  'featureCollection': dataset,
  'color': 'black',
  'width': 1
})

# Map.setCenter(-99.844, 37.649, 5)
Map.addLayer(image, visParams, 'TIGER/2018/Counties')
Map.addLayer(countyOutlines, {}, 'county outlines')
# Map.addLayer(dataset, {}, 'for Inspector', False)


dataset = ee.FeatureCollection('TIGER/2018/States')
visParams = {
  'palette': ['purple', 'blue', 'green', 'yellow', 'orange', 'red'],
  'min': 500000000.0,
  'max': 5e+11,
  'opacity': 0.8,
}
image = ee.Image().float().paint(dataset, 'ALAND')
# Map.setCenter(-99.844, 37.649, 5)
Map.addLayer(image, visParams, 'TIGER/2018/States')
# Map.addLayer(dataset, {}, 'for Inspector', False)
