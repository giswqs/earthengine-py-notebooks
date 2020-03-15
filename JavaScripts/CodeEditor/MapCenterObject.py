import ee 
from ee_plugin import Map 

# Center the map on an image.

image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20130603')
Map.addLayer(image, {'bands': ['B4',  'B3',  'B2'], 'max': 20000})
Map.centerObject(image)
