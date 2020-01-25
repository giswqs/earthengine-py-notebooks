# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Filter/filter_string_starts_with.py

import ee
from ee_plugin import Map


states = ee.FeatureCollection('TIGER/2018/States')

# Select states its name starting with 'Al'
selected = states.filter(ee.Filter.stringStartsWith('NAME', 'Al'))


Map.centerObject(selected, 6)
Map.addLayer(ee.Image().paint(selected, 0, 2), {'palette': 'yellow'}, 'Selected')
