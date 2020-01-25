# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Image/get_band_name_and_type.py

import ee
from ee_plugin import Map

roi = ee.Geometry.Point([-99.2182, 46.7824])

collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
    .filterBounds(roi) \
    .filter(ee.Filter.calendarRange(6, 6, 'month')) \
    .sort('DATE_ACQUIRED')

print(collection.size().getInfo())

first = ee.Image(collection.first())
print(first.bandNames().getInfo())
print(first.bandTypes().getInfo())
