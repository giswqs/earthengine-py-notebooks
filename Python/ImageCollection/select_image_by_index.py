# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/ImageCollection/select_image_by_index.py

import ee
from ee_plugin import Map

collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA')\
    .filter(ee.Filter.eq('WRS_PATH', 44))\
    .filter(ee.Filter.eq('WRS_ROW', 34))\
    .filterDate('2014-01-01', '2015-01-01')

image = ee.Image(collection.toList(collection.size()).get(0))  # select by index from 0 to size-1
print(image.get('system:id').getInfo())

Map.setCenter(-122.3578, 37.7726, 12)
Map.addLayer(image, {"bands": ['B4', 'B3', 'B2'], "max": 0.3}, 'median')
