import ee
from ee_plugin import Map

# This function gets NDVI from Landsat 8 imagery.


def addNDVI(image):
    return image.addBands(image.normalizedDifference(['B5', 'B4']))


# Load the Landsat 8 raw data, filter by location and date.
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1') \
    .filterBounds(ee.Geometry.Point(-122.262, 37.8719)) \
    .filterDate('2014-06-01', '2014-10-01')

# Map the function over the collection.
ndviCollection = collection.map(addNDVI)

first = ndviCollection.first()
print(first.getInfo())

bandNames = first.bandNames()
print(bandNames.getInfo())
