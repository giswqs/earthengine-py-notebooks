import ee 
from ee_plugin import Map 

# Load input imagery: Landsat 7 5-year composite.
image = ee.Image('LANDSAT/LE7_TOA_5YEAR/2008_2012')
# print(image.getInfo())

# Load an input region: Sierra Nevada.
region = ee.Feature(ee.FeatureCollection('EPA/Ecoregions/2013/L3') \
  .filter(ee.Filter.eq('us_l3name', 'Sierra Nevada')) \
  .first())

# Reduce the region. The region parameter is the Feature geometry.
meanDictionary = image.reduceRegion(**{
  'reducer': ee.Reducer.mean(),
  'geometry': region.geometry(),
  'scale': 30,
  'maxPixels': 1e9
})

# The result is a Dictionary.  Print it.
Map.centerObject(region, 9)
Map.addLayer(image, {'bands': ['B4', 'B3', 'B2']}, 'Landsat-7')
Map.addLayer(ee.Image().paint(region, 1, 3), {'palette': 'green'}, 'Mean Image')
print(meanDictionary.getInfo())
