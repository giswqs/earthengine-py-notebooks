# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/ImageCollection/filtering_by_calendar_range.py

import ee 
from ee_plugin import Map 

roi = ee.Geometry.Point([-99.2182, 46.7824])

# find images acquired during June and July
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
    .filterBounds(roi) \
    .filter(ee.Filter.calendarRange(6, 7, 'month')) \
    .sort('DATE_ACQUIRED')

print(collection.size().getInfo())

first = collection.first()
propertyNames = first.propertyNames()
print(propertyNames.getInfo())

time_start = ee.Date(first.get('system:time_start')).format("YYYY-MM-dd")
print(time_start.getInfo())