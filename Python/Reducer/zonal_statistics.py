import ee 
from ee_plugin import Map 

# Load a region representing the United States
region = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017') \
  .filter(ee.Filter.eq('country_na', 'United States'))

# Load MODIS land cover categories in 2001.
landcover = ee.Image('MODIS/051/MCD12Q1/2001_01_01') \
  .select('Land_Cover_Type_1')

# Load nightlights image inputs.
nl2001 = ee.Image('NOAA/DMSP-OLS/NIGHTTIME_LIGHTS/F152001') \
  .select('stable_lights')
nl2012 = ee.Image('NOAA/DMSP-OLS/NIGHTTIME_LIGHTS/F182012') \
  .select('stable_lights')

# Compute the nightlights decadal difference, add land cover codes.
nlDiff = nl2012.subtract(nl2001).addBands(landcover)

# Grouped a mean 'reducer': change of nightlights by land cover category.
means = nlDiff.reduceRegion(**{
  'reducer': ee.Reducer.mean().group(**{
    'groupField': 1,
    'groupName': 'code',
  }),
  'geometry': region.geometry(),
  'scale': 1000,
  'maxPixels': 1e8
})

# Print the resultant Dictionary.
print(means.getInfo())
