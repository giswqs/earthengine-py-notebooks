# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/FeatureCollection/add_random_value_column.py

import ee 
from ee_plugin import Map 

HUC10 = ee.FeatureCollection("USGS/WBD/2017/HUC10")
HUC08 = ee.FeatureCollection('USGS/WBD/2017/HUC08')
roi = HUC08.filter(ee.Filter.eq('name', 'Pipestem'))

# Map.centerObject(roi, 10)
# Map.addLayer(ee.Image().paint(roi, 0, 3), {}, 'HUC08')

# # select polygons intersecting the roi
roi2 = HUC10.filter(ee.Filter.contains(**{'leftValue': roi.geometry(), 'rightField': '.geo'}))
# Map.addLayer(ee.Image().paint(roi2, 0, 2), {'palette': 'blue'}, 'HUC10')

# roi = HUC10.filter(ee.Filter.stringContains(**{'leftField': 'huc10', 'rightValue': '10160002'}))
roi3 = roi2.randomColumn('random')
# # print(roi3)
# Map.addLayer(roi3)

print("Random value: ", roi3.first().get('random').getInfo())