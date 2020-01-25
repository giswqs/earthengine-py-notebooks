# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Visualization/random_color_visualizer.py

import ee
from ee_plugin import Map

dataset = ee.Image('USGS/NLCD/NLCD2016')
landcover = ee.Image(dataset.select('landcover'))

Map.setCenter(-95, 38, 5)
Map.addLayer(landcover.randomVisualizer(), {}, 'Landcover')
