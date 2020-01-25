# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/FeatureCollection/select_by_strings.py

import ee
from ee_plugin import Map

#!/usr/bin/env python
"""Select by strings

"""

# Select states with "A" in its name
fc = ee.FeatureCollection('TIGER/2018/States') \
    .filter(ee.Filter.stringContains('STUSPS', 'A'))

image = ee.Image().paint(fc, 0, 2)
Map.centerObject(fc, 6)
Map.addLayer(image, {'palette': 'FF0000'}, '*A*')


# Select states its name starting with 'A'
fc = ee.FeatureCollection('TIGER/2018/States') \
    .filter(ee.Filter.stringStartsWith('STUSPS', 'A'))

image = ee.Image().paint(fc, 0, 2)
Map.addLayer(image, {'palette': '0000FF'}, 'A*')
