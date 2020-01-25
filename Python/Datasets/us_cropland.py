# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Datasets/us_cropland.py

# Metadata: https://developers.google.com/earth-engine/datasets/catalog/USDA_NASS_CDL

import ee 
from ee_plugin import Map 

dataset = ee.ImageCollection('USDA/NASS/CDL') \
                  .filter(ee.Filter.date('2017-01-01', '2018-12-31')) \
                  .first()
cropLandcover = dataset.select('cropland')
Map.setCenter(-100.55, 40.71, 4)
Map.addLayer(cropLandcover, {}, 'Crop Landcover')
