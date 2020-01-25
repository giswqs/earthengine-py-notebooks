# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Filter/filter_range_contains.py

import ee 
from ee_plugin import Map 

import ee 
from ee_plugin import Map 

states = ee.FeatureCollection('TIGER/2018/States')
# print(states.first().getInfo())

# Select states with land area between 200,000 km2 and 300,000 km2
selected = states.filter(ee.Filter.rangeContains("ALAND", 200000000000, 300000000000))
Map.centerObject(selected, 6)
Map.addLayer(ee.Image().paint(selected, 0, 2), {'palette': 'yellow'}, 'Selected')