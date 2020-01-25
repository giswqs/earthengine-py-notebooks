import ee 
from ee_plugin import Map 

# Load a primary 'collection': Landsat imagery.
primary = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
    .filterDate('2014-04-01', '2014-06-01') \
    .filterBounds(ee.Geometry.Point(-122.092, 37.42))

# Load a secondary 'collection': MODIS imagery.
modSecondary = ee.ImageCollection('MODIS/006/MOD09GA') \
    .filterDate('2014-03-01', '2014-07-01')

# Define an allowable time difference: two days in milliseconds.
twoDaysMillis = 2 * 24 * 60 * 60 * 1000

# Create a time filter to define a match as overlapping timestamps.
timeFilter = ee.Filter.Or(
  ee.Filter.maxDifference(**{
    'difference': twoDaysMillis,
    'leftField': 'system:time_start',
    'rightField': 'system:time_end'
  }),
  ee.Filter.maxDifference(**{
    'difference': twoDaysMillis,
    'leftField': 'system:time_end',
    'rightField': 'system:time_start'
  })
)

# Define the join.
saveAllJoin = ee.Join.saveAll(**{
  'matchesKey': 'terra',
  'ordering': 'system:time_start',
  'ascending': True
})

# Apply the join.
landsatModis = saveAllJoin.apply(primary, modSecondary, timeFilter)

# Display the result.
print('Join.saveAll:', landsatModis.getInfo())

