import ee 
from ee_plugin import Map 

# Load and filter the Sentinel-2 image collection.
collection = ee.ImageCollection('COPERNICUS/S2') \
    .filterDate('2016-01-01', '2016-12-31') \
    .filterBounds(ee.Geometry.Point([-81.31, 29.90]))

# Reduce the collection.
extrema = collection.reduce(ee.Reducer.minMax())
# print(extrema.getInfo())
min_image = extrema.select(0)
max_image = extrema.select(1)

Map.setCenter(-81.31, 29.90, 10)
Map.addLayer(min_image, {}, 'Min image')
Map.addLayer(max_image, {}, 'Max image')