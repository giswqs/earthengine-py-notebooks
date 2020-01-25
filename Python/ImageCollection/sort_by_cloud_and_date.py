# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/ImageCollection/sort_by_cloud_and_date.py

import ee
from ee_plugin import Map

# This function masks the input with a threshold on the simple cloud score.


def cloudMask(img):
    cloudscore = ee.Algorithms.Landsat.simpleCloudScore(img).select('cloud')
    return img.updateMask(cloudscore.lt(50))


# Load a Landsat 5 image collection.
collection = ee.ImageCollection('LANDSAT/LT5_L1T_TOA') \
    .filterDate('2008-04-01', '2010-04-01') \
    .filterBounds(ee.Geometry.Point(-122.2627, 37.8735)) \
    .map(cloudMask) \
    .select(['B4', 'B3']) \
    .sort('system:time_start', True)  #Sort the collection in chronological order.

print(collection.size().getInfo())

first = collection.first().get('system:id')
print(first.getInfo())