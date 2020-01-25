# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/FeatureCollection/minimum_bounding_geometry.py

import ee 
from ee_plugin import Map 

HUC10 = ee.FeatureCollection("USGS/WBD/2017/HUC10")
HUC08 = ee.FeatureCollection('USGS/WBD/2017/HUC08')
roi = HUC08.filter(ee.Filter.eq('name', 'Pipestem'))

Map.centerObject(roi, 10)
Map.addLayer(ee.Image().paint(roi, 0, 1), {}, 'HUC8')

bound = ee.Geometry(roi.geometry()).bounds()
Map.addLayer(ee.Image().paint(bound, 0, 1), {'palette': 'red'}, "Minimum bounding geometry")
