import ee
from ee_plugin import Map

# This function returns the image centroid as a new Feature.


def getGeom(image):
    return ee.Feature(image.geometry().centroid(), {'foo': 1})


# Load a Landsat 8 collection.
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1') \
    .filterBounds(ee.Geometry.Point(-122.262, 37.8719)) \
    .filterDate('2014-06-01', '2014-10-01')

# Map the function over the ImageCollection.
featureCollection = ee.FeatureCollection(collection.map(getGeom))

# Map.setCenter(-122.1231, 37.8719, 12)
Map.centerObject(featureCollection, 15)
Map.addLayer(featureCollection, {'color': "yellow"}, "Image centroids")

# Print the collection.
# print(featureCollection)
