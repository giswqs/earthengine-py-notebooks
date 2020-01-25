import ee 
from ee_plugin import Map 

dataset = ee.ImageCollection('GLCF/GLS_WATER')
water = dataset.select('water').mosaic()
waterVis = {
  'min': 1.0,
  'max': 4.0,
  'palette': ['FAFAFA', '00C5FF', 'DF73FF', '828282', 'CCCCCC'],
}
Map.setCenter(-79.3094, 44.5693, 8)
Map.addLayer(water, waterVis, 'Water')
