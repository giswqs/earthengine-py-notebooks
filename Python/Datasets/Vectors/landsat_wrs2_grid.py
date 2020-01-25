# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Datasets/Vectors/landsat_wrs2_grid.py

import ee 
from ee_plugin import Map 

dataset = ee.FeatureCollection('projects/google/wrs2_descending')

empty = ee.Image().byte()

Map.setCenter(-78, 36, 8)
Map.addLayer(empty.paint(dataset, 0, 2), {}, 'Landsat WRS-2 grid')