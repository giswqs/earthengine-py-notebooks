import ee 
from ee_plugin import Map 

# Load US cenus data as a FeatureCollection.
census = ee.FeatureCollection('TIGER/2010/Blocks')

# Filter the collection to include only Benton County, OR.
benton = census.filter(
  ee.Filter.And(
    ee.Filter.eq('statefp10', '41'),
    ee.Filter.eq('countyfp10', '003')
  )
)

# Display Benton County cenus blocks.
Map.setCenter(-123.27, 44.57, 13)
Map.addLayer(ee.Image().paint(benton, 1, 3), {}, 'Benten County, OR')

# Compute sums of the specified properties.
properties = ['pop10', 'housing10']
sums = benton \
    .filter(ee.Filter.notNull(properties)) \
    .reduceColumns(**{
      'reducer': ee.Reducer.sum().repeat(2),
      'selectors': properties
    })

# Print the resultant Dictionary.
print(sums.getInfo())

