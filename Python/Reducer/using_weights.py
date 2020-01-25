import ee 
from ee_plugin import Map 

# Load an input Landsat 8 image.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_186059_20130419')

# Compute cloud score and reverse it such that the highest
# weight (100) is for the least cloudy pixels.
cloudWeight = ee.Image(100).subtract(
  ee.Algorithms.Landsat.simpleCloudScore(image).select(['cloud']))

# Compute NDVI and add the cloud weight band.
ndvi = image.normalizedDifference(['B5', 'B4']).addBands(cloudWeight)

# Define an arbitrary region in a cloudy area.
region = ee.Geometry.Rectangle(9.9069, 0.5981, 10.5, 0.9757)

# Use a mean reducer.
reducer = ee.Reducer.mean()

# Compute the unweighted mean.
unweighted = ndvi.select(['nd']).reduceRegion(reducer, region, 30)

# compute mean weighted by cloudiness.
weighted = ndvi.reduceRegion(reducer.splitWeights(), region, 30)

# Observe the difference as a result of weighting by cloudiness.
print('unweighted:', unweighted.getInfo())
print('weighted:', weighted.getInfo())

