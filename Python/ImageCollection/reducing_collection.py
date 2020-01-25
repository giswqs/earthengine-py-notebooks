import ee 
from ee_plugin import Map 


def addTime(image):
    return image.addBands(image.metadata('system:time_start').divide(1000 * 60 * 60 * 24 * 365))

# Load a Landsat 8 collection for a single path-row.
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
    .filter(ee.Filter.eq('WRS_PATH', 44)) \
    .filter(ee.Filter.eq('WRS_ROW', 34)) \
    .filterDate('2014-01-01', '2015-01-01')

# Compute a median image and display.
median = collection.median()
Map.setCenter(-122.3578, 37.7726, 12)
Map.addLayer(median, {'bands': ['B4', 'B3', 'B2'], 'max': 0.3}, 'median')


# Reduce the collection with a median reducer.
median = collection.reduce(ee.Reducer.median())

# Display the median image.
Map.addLayer(median,
             {'bands': ['B4_median', 'B3_median', 'B2_median'], 'max': 0.3},
             'also median')


# # This function adds a band representing the image timestamp.
# addTime = function(image) {
#   return image.addBands(image.metadata('system:time_start')
#     # Convert milliseconds from epoch to years to aid in
#     # interpretation of the following trend calculation. \
#     .divide(1000 * 60 * 60 * 24 * 365))
# }

# Load a MODIS collection, filter to several years of 16 day mosaics,
# and map the time band function over it.
collection = ee.ImageCollection('MODIS/006/MYD13A1') \
  .filterDate('2004-01-01', '2010-10-31') \
  .map(addTime)

# Select the bands to model with the independent variable first.
trend = collection.select(['system:time_start', 'EVI']) \
  .reduce(ee.Reducer.linearFit())

# Display the trend with increasing slopes in green, decreasing in red.
Map.setCenter(-96.943, 39.436, 5)
Map.addLayer(
    trend,
    {'min': 0, 'max': [-100, 100, 10000], 'bands': ['scale', 'scale', 'offset']},
    'EVI trend')

