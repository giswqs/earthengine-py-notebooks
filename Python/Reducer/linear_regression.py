import ee 
from ee_plugin import Map 

# This function adds a time band to the image.

def createTimeBand(image):
    return image.addBands(image.metadata('system:time_start').divide(1e18))

# createTimeBand = function(image) {
#   # Scale milliseconds by a large constant to avoid very small slopes
#   # in the linear regression output.
#   return image.addBands(image.metadata('system:time_start').divide(1e18))
# }

# Load the input image 'collection': projected climate data.
collection = ee.ImageCollection('NASA/NEX-DCP30_ENSEMBLE_STATS') \
  .filter(ee.Filter.eq('scenario', 'rcp85')) \
  .filterDate(ee.Date('2006-01-01'), ee.Date('2050-01-01')) \
  .map(createTimeBand)

# Reduce the collection with the linear fit reducer.
# Independent variable are followed by dependent variables.
linearFit = collection.select(['system:time_start', 'pr_mean']) \
  .reduce(ee.Reducer.linearFit())

# Display the results.
Map.setCenter(-100.11, 40.38, 5)
Map.addLayer(linearFit,
  {'min': 0, 'max': [-0.9, 8e-5, 1], 'bands': ['scale', 'offset', 'scale']}, 'fit')

