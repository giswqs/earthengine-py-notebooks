# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/FeatureCollection/column_statistics.py

import ee 
from ee_plugin import Map 

fromFT = ee.FeatureCollection("users/wqs/Pipestem/Pipestem_HUC10")
geom = fromFT.geometry()
Map.centerObject(fromFT)
Map.addLayer(ee.Image().paint(geom, 0, 2), {}, 'Watersheds')

print(fromFT.aggregate_stats('AreaSqKm'))

total_area = fromFT.reduceColumns(**{
  'reducer': ee.Reducer.sum(),
  'selectors': ['AreaSqKm']
  # weightSelectors: ['weight']
}).getInfo()

print("Total area: ", total_area)
