import ee 
from ee_plugin import Map 

# Load input imagery: Landsat 7 5-year composite.
image = ee.Image('LANDSAT/LE7_TOA_5YEAR/2008_2012')

# Load a FeatureCollection of counties in Maine.
maineCounties = ee.FeatureCollection('TIGER/2016/Counties') \
  .filter(ee.Filter.eq('STATEFP', '23'))

# Add reducer output to the Features in the collection.
maineMeansFeatures = image.reduceRegions(**{
  'collection': maineCounties,
  'reducer': ee.Reducer.mean(),
  'scale': 30,
})

feature = ee.Feature(maineMeansFeatures.first()).select(image.bandNames())
# print(feature.getInfo())
properties = feature.propertyNames()

# Print the first feature, to illustrate the result.
print(feature.toDictionary(properties).getInfo())

