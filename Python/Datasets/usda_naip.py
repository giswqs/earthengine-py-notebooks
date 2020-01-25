import ee 
from ee_plugin import Map 

roi = ee.FeatureCollection('TIGER/2018/States') \
  .filter(ee.Filter.eq('STUSPS', 'ND'));

dataset = ee.ImageCollection('USDA/NAIP/DOQQ') \
                  .filter(ee.Filter.date('2016-01-01', '2017-12-31'))\
                  .filterBounds(roi)
TrueColor = dataset.select(['N', 'R', 'G']).mosaic()
TrueColorVis = {
  'min': 0.0,
  'max': 255.0,
}
# Map.setCenter(-73.9958, 40.7278, 15)
Map.centerObject(roi, 8)
Map.addLayer(TrueColor, TrueColorVis, 'True Color')
