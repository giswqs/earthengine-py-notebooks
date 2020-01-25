# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Visualization/color_by_attribute.py

import ee 
from ee_plugin import Map 

fc = ee.FeatureCollection('TIGER/2018/States') 

print(fc.first().getInfo())

# Use this empty image for paint().
empty = ee.Image().byte()
palette = ['green', 'yellow', 'orange', 'red']

states = empty.paint(**{
  'featureCollection': fc,
  'color': 'ALAND',
})

Map.addLayer(states, {'palette': palette}, 'US States')