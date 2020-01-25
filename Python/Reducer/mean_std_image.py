import ee 
from ee_plugin import Map 

# Load a Landsat 8 image.
image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318')

# Combine the mean and standard deviation reducers.
reducers = ee.Reducer.mean().combine(**{
  'reducer2': ee.Reducer.stdDev(),
  'sharedInputs': True
})

# Use the combined reducer to get the mean and SD of the image.
stats = image.reduceRegion(**{
  'reducer': reducers,
  'bestEffort': True,
})

# Display the dictionary of band means and SDs.
print(stats.getInfo())

