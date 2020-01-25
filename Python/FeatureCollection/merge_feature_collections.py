# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/FeatureCollection/merge_feature_collections.py

import ee
from ee_plugin import Map


SD = ee.FeatureCollection('TIGER/2018/States') \
    .filter(ee.Filter.eq('STUSPS', 'SD'))

ND = ee.FeatureCollection('TIGER/2018/States') \
    .filter(ee.Filter.eq('STUSPS', 'ND'))

states = SD.merge(ND)
Map.centerObject(states, 6)
Map.addLayer(ee.Image().paint(states, 0, 2), {}, 'Dakotas')
# print(states.size().getInfo())
