# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/ImageCollection/filtering_by_metadata.py

import ee
from ee_plugin import Map

region = ee.Geometry.Polygon(
    [[[121.89674377441406, 11.91539248304918],
      [121.98291778564453, 11.93218823174339],
      [121.95236206054688, 12.020516709145957],
      [121.86378679003906, 12.006748772470699]]])

# Image Collection
collection = ee.ImageCollection('COPERNICUS/S2') \
    .filterDate('2017-03-01', '2017-04-04') \
    .filterBounds(region) \
    .filterMetadata('CLOUDY_PIXEL_PERCENTAGE', 'less_than', 20)
# Map.addLayer(collection, {'min': 0, 'max': 3000,
#                           'bands': ["B4", "B3", "B2"]}, 'TOA')
print(collection.size().getInfo())

first = collection.first()
Map.centerObject(first, 10)
Map.addLayer(first, {'min': 0, 'max': 3000,
                     'bands': ["B4", "B3", "B2"]}, 'TOA')
