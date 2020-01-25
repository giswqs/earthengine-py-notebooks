import ee
from ee_plugin import Map

# This function gets NDVI from a Landsat 8 image.


def addNDVI(image):
    return image.addBands(image.normalizedDifference(['B5', 'B4']))

# This function masks cloudy pixels.


def cloudMask(image):
    clouds = ee.Algorithms.Landsat.simpleCloudScore(image).select(['cloud'])
    return image.updateMask(clouds.lt(10))


# Load a Landsat collection, map the NDVI and cloud masking functions over it.
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
    .filterBounds(ee.Geometry.Point([-122.262, 37.8719])) \
    .filterDate('2014-03-01', '2014-05-31') \
    .map(addNDVI) \
    .map(cloudMask)

# Reduce the collection to the mean of each pixel and display.
meanImage = collection.reduce(ee.Reducer.mean())
vizParams = {'bands': ['B5_mean', 'B4_mean', 'B3_mean'], 'min': 0, 'max': 0.5}
Map.setCenter(-122.262, 37.8719, 10)
Map.addLayer(meanImage, vizParams, 'mean')

# Load a region in which to compute the mean and display it.
counties = ee.FeatureCollection('TIGER/2016/Counties')
santaClara = ee.Feature(counties.filter(
    ee.Filter.eq('NAME', 'Santa Clara')).first())
Map.addLayer(ee.Image().paint(santaClara, 0, 2), {
             'palette': 'yellow'}, 'Santa Clara')

# Get the mean of NDVI in the region.
mean = meanImage.select(['nd_mean']).reduceRegion(**{
    'reducer': ee.Reducer.mean(),
    'geometry': santaClara.geometry(),
    'scale': 30
})

# Print mean NDVI for the region.
print('Santa Clara spring mean NDVI:', mean.get('nd_mean').getInfo())
