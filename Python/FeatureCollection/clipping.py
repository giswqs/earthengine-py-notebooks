# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/FeatureCollection/clipping.py

import ee 
from ee_plugin import Map 

roi = ee.Geometry.Polygon(
        [[[-73.99891354682285, 40.74560250077625],
          [-73.99891354682285, 40.74053023068626],
          [-73.98749806525547, 40.74053023068626],
          [-73.98749806525547, 40.74560250077625]]])


fc = ee.FeatureCollection('TIGER/2016/Roads').filterBounds(roi)

clipped = fc.map(lambda f: f.intersection(roi))

Map.centerObject(ee.FeatureCollection(roi), 17)
Map.addLayer(ee.Image().paint(roi, 0, 2), {'palette': 'yellow'}, 'ROI')
# Map.setCenter(-73.9596, 40.7688, 12)
Map.addLayer(ee.Image().paint(clipped, 0, 3), {'palette': 'red'}, 'clipped')
Map.addLayer(fc, {}, 'Census roads', False)




