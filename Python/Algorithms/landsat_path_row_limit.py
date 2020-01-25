# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Algorithms/landsat_path_row_limit.py

import ee 
from ee_plugin import Map 

point = ee.Geometry.Point(-98.7011, 47.2624)
collection = ee.ImageCollection('LANDSAT/LC8_L1T_TOA') \
  .filterBounds(point) \
  .filterDate('2016-01-01', '2018-12-31')

# print(collection)

new_col = ee.Algorithms.Landsat.pathRowLimit(collection, 15, 100)
# print(new_col)

median = new_col.median()
vis = {'bands': ['B5', 'B4', 'B3'], 'max': 0.3}

Map.setCenter(-98.7011, 47.2624, 10)
Map.addLayer(median, vis, 'Median')
