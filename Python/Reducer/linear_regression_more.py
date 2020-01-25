import ee 
from ee_plugin import Map 

# This function adds a time band to the image.

def createTimeBand(image):
    return image.addBands(image.metadata('system:time_start').divide(1e18))

# createTimeBand = function(image) {
#   # Scale milliseconds by a large constant.
#   return image.addBands(image.metadata('system:time_start').divide(1e18))
# }

# This function adds a constant band to the image.
def createConstantBand(image):
    return ee.Image(1).addBands(image)
# createConstantBand = function(image) {
#   return ee.Image(1).addBands(image)
# }

# Load the input image 'collection': projected climate data.
collection = ee.ImageCollection('NASA/NEX-DCP30_ENSEMBLE_STATS') \
  .filterDate(ee.Date('2006-01-01'), ee.Date('2099-01-01')) \
  .filter(ee.Filter.eq('scenario', 'rcp85')) \
  .map(createTimeBand) \
  .map(createConstantBand) \
  .select(['constant', 'system:time_start', 'pr_mean', 'tasmax_mean'])

# Compute ordinary least squares regression coefficients.
linearRegression = collection.reduce(
  ee.Reducer.linearRegression(**{
    'numX': 2,
    'numY': 2
}))

# Compute robust linear regression coefficients.
robustLinearRegression = collection.reduce(
  ee.Reducer.robustLinearRegression(**{
    'numX': 2,
    'numY': 2
}))

# The results are array images that must be flattened for display.
# These lists label the information along each axis of the arrays.
bandNames = [['constant', 'time'], # 0-axis variation.
                 ['precip', 'temp']] # 1-axis variation.

# Flatten the array images to get multi-band images according to the labels.
lrImage = linearRegression.select(['coefficients']).arrayFlatten(bandNames)
rlrImage = robustLinearRegression.select(['coefficients']).arrayFlatten(bandNames)

# Display the OLS results.
Map.setCenter(-100.11, 40.38, 5)
Map.addLayer(lrImage,
  {'min': 0, 'max': [-0.9, 8e-5, 1], 'bands': ['time_precip', 'constant_precip', 'time_precip']}, 'OLS')

# Compare the results at a specific point:
print('OLS estimates:', lrImage.reduceRegion(**{
  'reducer': ee.Reducer.first(),
  'geometry': ee.Geometry.Point([-96.0, 41.0]),
  'scale': 1000
}).getInfo())

print('Robust estimates:', rlrImage.reduceRegion(**{
  'reducer': ee.Reducer.first(),
  'geometry': ee.Geometry.Point([-96.0, 41.0]),
  'scale': 1000
}).getInfo())

