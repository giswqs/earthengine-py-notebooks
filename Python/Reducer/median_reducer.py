import ee 
from ee_plugin import Map 

# Load an image collection, filtered so it's not too much data.
collection = ee.ImageCollection('LANDSAT/LT05/C01/T1') \
  .filterDate('2008-01-01', '2008-12-31') \
  .filter(ee.Filter.eq('WRS_PATH', 44)) \
  .filter(ee.Filter.eq('WRS_ROW', 34))

# Compute the median in each band, each pixel.
# Band names are B1_median, B2_median, etc.
median = collection.reduce(ee.Reducer.median())

# The output is an Image.  Add it to the map.
vis_param = {'bands': ['B4_median', 'B3_median', 'B2_median'], 'gamma': 1.6}
Map.setCenter(-122.3355, 37.7924, 9)
Map.addLayer(median, vis_param, 'Median')

