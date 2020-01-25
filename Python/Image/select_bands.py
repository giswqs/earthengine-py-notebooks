# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Image/select_bands.py

import ee
from ee_plugin import Map

# Load an image.
image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318')

band345 = image.select(['B[3-5]'])

bandNames = band345.bandNames()

print(bandNames.getInfo())

# Define visualization parameters in an object literal.
vizParams = {'bands': ['B5', 'B4', 'B3'],
             'min': 5000, 'max': 15000, 'gamma': 1.3}

# Center the map on the image and display.
Map.centerObject(image, 9)
Map.addLayer(band345, vizParams, 'Landsat 8 False color')
