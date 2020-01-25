# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/FeatureCollection/column_statistics_multiple.py

import ee 
from ee_plugin import Map 

fromFT = ee.FeatureCollection("users/wqs/Pipestem/Pipestem_HUC10")
geom = fromFT.geometry()
Map.centerObject(fromFT)
Map.addLayer(ee.Image().paint(geom, 0, 2), {}, 'Watersheds')

stats = fromFT.reduceColumns(**{
  'reducer': ee.Reducer.sum().repeat(2),
  'selectors': ['AreaSqKm', 'AreaAcres']
  # weightSelectors: ['weight']
}).getInfo()

print(stats)
