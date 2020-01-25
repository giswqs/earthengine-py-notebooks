import ee 
from ee_plugin import Map 

# Load a Landsat 8 image collection at a point of interest.
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
    .filterBounds(ee.Geometry.Point(-122.09, 37.42))

# Define start and end dates with which to filter the collections.
april = '2014-04-01'
may = '2014-05-01'
june = '2014-06-01'
july = '2014-07-01'

# The primary collection is Landsat images from April to June.
primary = collection.filterDate(april, june)

# The secondary collection is Landsat images from May to July.
secondary = collection.filterDate(may, july)

# Use an equals filter to define how the collections match.
filter = ee.Filter.equals(**{
  'leftField': 'system:index',
  'rightField': 'system:index'
})

# Define the join.
invertedJoin = ee.Join.inverted()

# Apply the join.
invertedJoined = invertedJoin.apply(primary, secondary, filter)

# Display the result.
print('Inverted join: ', invertedJoined.getInfo())

