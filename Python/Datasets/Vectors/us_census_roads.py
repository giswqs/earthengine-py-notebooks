# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Datasets/Vectors/us_census_roads.py

import ee 
from ee_plugin import Map 

fc = ee.FeatureCollection('TIGER/2016/Roads')
Map.setCenter(-73.9596, 40.7688, 12)
Map.addLayer(fc, {}, 'Census roads')
