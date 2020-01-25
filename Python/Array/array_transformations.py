import ee 
import math
from ee_plugin import Map 

# This function masks the input with a threshold on the simple cloud score.
def cloudMask(img):
  cloudscore = ee.Algorithms.Landsat.simpleCloudScore(img).select('cloud')
  return img.updateMask(cloudscore.lt(50))

# cloudMask = function(img) {
#   cloudscore = ee.Algorithms.Landsat.simpleCloudScore(img).select('cloud')
#   return img.updateMask(cloudscore.lt(50))
# }

# This function computes the predictors and the response from the input.
def makeVariables(image):
  # Compute time of the image in fractional years relative to the Epoch.
  year = ee.Image(image.date().difference(ee.Date('1970-01-01'), 'year'))
  # Compute the season in radians, one cycle per year.
  season = year.multiply(2 * math.pi)
  # Return an image of the predictors followed by the response.
  return image.select() \
    .addBands(ee.Image(1)) \
    .addBands(year.rename('t')) \
    .addBands(season.sin().rename('sin')) \
    .addBands(season.cos().rename('cos')) \
    .addBands(image.normalizedDifference().rename('NDVI')) \
    .toFloat()

# Load a Landsat 5 image collection.
collection = ee.ImageCollection('LANDSAT/LT05/C01/T1_TOA') \
  .filterDate('2008-04-01', '2010-04-01')   \
  .filterBounds(ee.Geometry.Point(-122.2627, 37.8735)) \
  .map(cloudMask)  \
  .select(['B4', 'B3']) \
  .sort('system:time_start', True)

# # This function computes the predictors and the response from the input.
# makeVariables = function(image) {
#   # Compute time of the image in fractional years relative to the Epoch.
#   year = ee.Image(image.date().difference(ee.Date('1970-01-01'), 'year'))
#   # Compute the season in radians, one cycle per year.
#   season = year.multiply(2 * Math.PI)
#   # Return an image of the predictors followed by the response.
#   return image.select() \
#     .addBands(ee.Image(1))                                  # 0. constant \
#     .addBands(year.rename('t'))                             # 1. linear trend \
#     .addBands(season.sin().rename('sin'))                   # 2. seasonal \
#     .addBands(season.cos().rename('cos'))                   # 3. seasonal \
#     .addBands(image.normalizedDifference().rename('NDVI'))  # 4. response \
#     .toFloat()
# }

# Define the axes of variation in the collection array.
imageAxis = 0
bandAxis = 1

# Convert the collection to an array.
array = collection.map(makeVariables).toArray()

# Check the length of the image axis (number of images).
arrayLength = array.arrayLength(imageAxis)
# Update the mask to ensure that the number of images is greater than or
# equal to the number of predictors (the linear model is solveable).
array = array.updateMask(arrayLength.gt(4))

# Get slices of the array according to positions along the band axis.
predictors = array.arraySlice(bandAxis, 0, 4)
response = array.arraySlice(bandAxis, 4)

# Compute coefficients the easiest way.
coefficients3 = predictors.matrixSolve(response)

# Turn the results into a multi-band image.
coefficientsImage = coefficients3 \
  .arrayProject([0]) \
  .arrayFlatten([
    ['constant', 'trend', 'sin', 'cos']
])

print(coefficientsImage.getInfo())
Map.setCenter(-122.2627, 37.8735, 10)
Map.addLayer(coefficientsImage, {}, 'coefficientsImage')