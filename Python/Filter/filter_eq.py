# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Filter/filter_eq.py
# Filter to metadata equal to the given value.

import ee 
from ee_plugin import Map 

states = ee.FeatureCollection('TIGER/2018/States')

selected = states.filter(ee.Filter.eq("NAME", 'California'))

Map.centerObject(selected, 6)
Map.addLayer(ee.Image().paint(selected, 0, 2), {'palette': 'yellow'}, 'Selected')