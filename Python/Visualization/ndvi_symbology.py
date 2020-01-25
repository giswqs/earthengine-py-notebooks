# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Visualization/ndvi_symbology.py

import ee
from ee_plugin import Map

# This function gets NDVI from Landsat 5 imagery.


def getNDVI(image):
    return image.normalizedDifference(['B4', 'B3'])


image1 = ee.Image('LANDSAT/LT05/C01/T1_TOA/LT05_044034_19900604')

# Compute NDVI from the scene.
ndvi1 = getNDVI(image1)

ndviParams = {'palette': ['#d73027', '#f46d43', '#fdae61',
                          '#fee08b', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850']}

Map.centerObject(image1, 10)
Map.addLayer(ndvi1, ndviParams, 'NDVI')
