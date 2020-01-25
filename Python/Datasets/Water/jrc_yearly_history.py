import ee 
from ee_plugin import Map 

dataset = ee.ImageCollection('JRC/GSW1_1/YearlyHistory') \
                  .filter(ee.Filter.date('2015-01-01', '2015-12-31'))
waterClass = dataset.select('waterClass')
waterClassVis = {
  'min': 0.0,
  'max': 3.0,
  'palette': ['cccccc', 'ffffff', '99d9ea', '0000ff'],
}
Map.setCenter(59.414, 45.182, 7)
Map.addLayer(waterClass, waterClassVis, 'Water Class')
