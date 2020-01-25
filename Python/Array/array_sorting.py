import ee 
from ee_plugin import Map 

# Define an arbitrary region of interest as a point.
roi = ee.Geometry.Point(-122.26032, 37.87187)

# Use these bands.
bandNames = ee.List(['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'B11'])

# Load a Landsat 8 collection.
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
  .select(bandNames) \
  .filterBounds(roi) \
  .filterDate('2014-06-01', '2014-12-31') \
  .map(lambda image: ee.Algorithms.Landsat.simpleCloudScore(image))

# Convert the collection to an array.
array = collection.toArray()

# Label of the axes.
imageAxis = 0
bandAxis = 1

# Get the cloud slice and the bands of interest.
bands = array.arraySlice(bandAxis, 0, bandNames.length())
clouds = array.arraySlice(bandAxis, bandNames.length())

# Sort by cloudiness.
sorted = bands.arraySort(clouds)

# Get the least cloudy images, 20% of the total.
numImages = sorted.arrayLength(imageAxis).multiply(0.2).int()
leastCloudy = sorted.arraySlice(imageAxis, 0, numImages)

# Get the mean of the least cloudy images by reducing along the image axis.
mean = leastCloudy.arrayReduce(**{
  'reducer': ee.Reducer.mean(),
  'axes': [imageAxis]
})

# Turn the reduced array image into a multi-band image for display.
meanImage = mean.arrayProject([bandAxis]).arrayFlatten([bandNames])
Map.centerObject(ee.FeatureCollection(roi), 12)
Map.addLayer(meanImage, {'bands': ['B5', 'B4', 'B2'], 'min': 0, 'max': 0.5}, 'Mean Image')

