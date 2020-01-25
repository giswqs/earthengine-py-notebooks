import ee 
from ee_plugin import Map 

# Load a collection of US counties.
counties = ee.FeatureCollection('TIGER/2018/Counties')

# Make an image out of the land area attribute.
landAreaImg = counties \
  .filter(ee.Filter.notNull(['ALAND'])) \
  .reduceToImage(**{
    'properties': ['ALAND'],
    'reducer': ee.Reducer.first()
})

# Display the county land area image.
Map.setCenter(-99.976, 40.38, 5)
Map.addLayer(landAreaImg, {
  'min': 3e8,
  'max': 1.5e10,
  'palette': ['FCFDBF', 'FDAE78', 'EE605E', 'B63679', '711F81', '2C105C']
}, 'Land Area')
