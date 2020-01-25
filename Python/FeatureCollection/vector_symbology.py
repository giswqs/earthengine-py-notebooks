# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/FeatureCollection/vector_symbology.py

import ee
from ee_plugin import Map

fc = ee.FeatureCollection('TIGER/2018/States')
# .filter(ee.Filter.eq('STUSPS', 'MN'))

image = ee.Image().paint(**{
    'featureCollection': fc,
    'color': 1,
    'width': 3
})

Map.setCenter(-99.844, 37.649, 5)
Map.addLayer(image, {'palette': 'FF0000'}, 'TIGER/2018/States')
# Map.addLayer(fc, {}, 'US States')
