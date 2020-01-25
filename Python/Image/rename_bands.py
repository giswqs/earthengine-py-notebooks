# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Image/rename_bands.py

import ee 
from ee_plugin import Map 

image = ee.Image('LANDSAT/LC8_L1T/LC80260412017023LGN00')
b5 = image.select('B5')

Map.centerObject(image, 10)
Map.addLayer(image, {}, 'Band 5')

selected = image.select(["B5", 'B4', 'B3'], ['Nir', 'Red', 'Green'])
Map.addLayer(selected, {}, "Renamed bands")
print(selected.bandNames().getInfo())

