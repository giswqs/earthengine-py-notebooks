# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Datasets/Vectors/international_boundary.py

import ee 
from ee_plugin import Map 

# LSIB: Large Scale International Boundary Polygons, Simplified

# dataset = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
# styleParams = {
#   'fillColor': 'b5ffb4',
#   'color': '00909F',
#   'width': 3.0,
# }
# countries = dataset.style(**styleParams)
# Map.addLayer(countries, {}, 'USDOS/LSIB_SIMPLE/2017')


# LSIB: Large Scale International Boundary Polygons, Detailed
dataset = ee.FeatureCollection('USDOS/LSIB/2013')
visParams = {
  'palette': ['f5ff64', 'b5ffb4', 'beeaff', 'ffc0e8', '8e8dff', 'adadad'],
  'min': 0.0,
  'max': 894.0,
  'opacity': 0.8,
}
image = ee.Image().float().paint(dataset, 'iso_num')
Map.addLayer(image, visParams, 'USDOS/LSIB/2013')
# Map.addLayer(dataset, {}, 'for Inspector', False)
