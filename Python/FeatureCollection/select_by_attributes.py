# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/FeatureCollection/select_by_attributes.py

#!/usr/bin/env python
"""Select by attributes

"""

import ee
from ee_plugin import Map

# Select North Dakota and South Dakota
fc = ee.FeatureCollection('TIGER/2018/States') \
    .filter(ee.Filter.Or(
        ee.Filter.eq('STUSPS', 'ND'),
        ee.Filter.eq('STUSPS', 'SD'),
    ))

image = ee.Image().paint(fc, 0, 2)
# Map.setCenter(-99.844, 37.649, 5)
Map.centerObject(fc, 6)
Map.addLayer(image, {'palette': 'FF0000'}, 'TIGER/2018/States')


