import ee
from ee_plugin import Map

# Load an image.
image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318')

# Center the map on the image.
Map.centerObject(image, 9)

# Display the image.
Map.addLayer(image, {}, 'Landsat 8 original image')

# Define visualization parameters in an object literal.
vizParams = {'bands': ['B5', 'B4', 'B3'],
             'min': 5000, 'max': 15000, 'gamma': 1.3}

# Center the map on the image and display.
Map.centerObject(image, 9)
Map.addLayer(image, vizParams, 'Landsat 8 False color')

# Use Map.addLayer() to add features and feature collections to the map. For example,
counties = ee.FeatureCollection('TIGER/2016/Counties')
Map.addLayer(ee.Image().paint(counties, 0, 2), {}, 'counties')
