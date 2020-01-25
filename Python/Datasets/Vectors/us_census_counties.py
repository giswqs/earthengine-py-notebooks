# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Datasets/Vectors/us_census_counties.py

#!/usr/bin/env python
"""Display US Counties.

"""

# import datetime
import ee
from ee_plugin import Map

Map.setCenter(-110, 40, 5)
states = ee.FeatureCollection('TIGER/2018/States')
    # .filter(ee.Filter.eq('STUSPS', 'MN'))
# // Turn the strings into numbers
states = states.map(lambda f: f.set('STATEFP', ee.Number.parse(f.get('STATEFP'))))

state_image = ee.Image().float().paint(states, 'STATEFP')

visParams = {
  'palette': ['purple', 'blue', 'green', 'yellow', 'orange', 'red'],
  'min': 0,
  'max': 50,
  'opacity': 0.8,
};

counties = ee.FeatureCollection('TIGER/2016/Counties')  

image = ee.Image().paint(states, 0, 2)
Map.setCenter(-99.844, 37.649, 5)
# Map.addLayer(image, {'palette': 'FF0000'}, 'TIGER/2018/States')
Map.addLayer(image, visParams, 'TIGER/2016/States');
Map.addLayer(ee.Image().paint(counties, 0, 1), {}, 'TIGER/2016/Counties')
