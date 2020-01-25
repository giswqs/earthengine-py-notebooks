import ee 
from ee_plugin import Map 

dataset = ee.ImageCollection('JRC/GSW1_1/MonthlyHistory') \
                  .filter(ee.Filter.date('2015-01-01', '2015-12-31'))
water = dataset.select('water').mosaic()
waterVis = {
  'min': 0.0,
  'max': 2.0,
  'palette': ['ffffff', 'fffcb8', '0905ff'],
}
Map.setCenter(-58.999, -3.373, 7)
Map.addLayer(water, waterVis, 'Water')
