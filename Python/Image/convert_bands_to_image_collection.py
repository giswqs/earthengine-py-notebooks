# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Image/convert_bands_to_image_collection.py

import ee 
from ee_plugin import Map 

image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318')
print("Number of bands:", image.bandNames().size().getInfo())
imageCollection = ee.ImageCollection(image.bandNames().map(lambda b: image.select([b])))

print("ImageCollection size: ", imageCollection.size().getInfo())
