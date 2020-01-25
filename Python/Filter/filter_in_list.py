# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Filter/filter_in_list.py
# Filter on metadata contained in a list

import ee 
from ee_plugin import Map 

states = ee.FeatureCollection('TIGER/2018/States')

selected = states.filter(ee.Filter.inList("NAME", ['California', 'Nevada', 'Utah', 'Arizona']))

Map.centerObject(selected, 6)
Map.addLayer(ee.Image().paint(selected, 0, 2), {'palette': 'yellow'}, 'Selected')