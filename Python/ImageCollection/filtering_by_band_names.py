# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/ImageCollection/filtering_by_band_names.py

import ee
from ee_plugin import Map

roi = ee.Geometry.Point([-99.2182, 46.7824])


collection = ee.ImageCollection('USDA/NAIP/DOQQ') \
    .filterBounds(roi) \
    .filter(ee.Filter.listContains("system:band_names", "N"))
print(collection.size().getInfo())

first = collection.first()
Map.centerObject(first, 13)
Map.addLayer(first, {'bands': ['N', 'R', 'G']}, 'NAIP')