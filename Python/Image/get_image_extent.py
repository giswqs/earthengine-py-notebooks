# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Image/get_image_extent.py

import ee
from ee_plugin import Map

image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318')

# Define visualization parameters in an object literal.
vizParams = {'bands': ['B5', 'B4', 'B3'],
             'min': 5000, 'max': 15000, 'gamma': 1.3}

# Center the map on the image and display.
Map.centerObject(image, 9)
Map.addLayer(image, vizParams, 'Landsat 8 False color')

extent = image.geometry()
outline = ee.Image().paint(extent, 0, 2)
Map.addLayer(outline, {'palette': "yellow"}, "Image extent")

coordinates = extent.coordinates()

print(coordinates.getInfo())
