# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Visualization/landsat_symbology.py

import ee 
from ee_plugin import Map 

geometry = ee.Geometry.Point([-122.30287513732901, 37.441115780341605])

landsat = ee.ImageCollection("LANDSAT/LC08/C01/T1") \
    .filterDate('2016-01-01', '2017-01-01') \
    .filterBounds(geometry)

composite = ee.Algorithms.Landsat.simpleComposite(**{
  'collection': landsat,
  'asFloat': True
})

rgbVis = {'bands': ["B4", "B3", "B2"], 'min':0, 'max': 0.3}
nirVis = {'bands': ["B5", "B4", "B3"], 'min':0, 'max': [0.5, 0.3, 0.3]}
tempVis = {'bands': ["B10"], 'min': 280, 'max': 310, 'palette': ["blue", "red", "orange", "yellow"]}

Map.addLayer(composite, rgbVis, "RGB")
Map.addLayer(composite, nirVis, "False Color")
Map.addLayer(composite, tempVis, "Thermal")

Map.centerObject(ee.FeatureCollection(geometry), 10)
