import ee 
from ee_plugin import Map 

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

Map.setCenter(-99.844, 37.649, 5)
Map.addLayer(image, visParams, 'TIGER/2018/Counties')
Map.addLayer(countyOutlines, {}, 'county outlines')
# Map.addLayer(dataset, {}, 'for Inspector', False)