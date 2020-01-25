# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Filter/filter_string_ends_with.py

import ee 
from ee_plugin import Map 

states = ee.FeatureCollection('TIGER/2018/States')

# Select states with its name ending with 'ia'
selected = states.filter(ee.Filter.stringEndsWith('NAME', 'ia'))


Map.centerObject(selected, 6)
Map.addLayer(ee.Image().paint(selected, 0, 2), {'palette': 'yellow'}, 'Selected')
