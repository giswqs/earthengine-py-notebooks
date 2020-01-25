import ee 
from ee_plugin import Map 

# Load a primary 'collection': Landsat imagery.
primary = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
    .filterDate('2014-04-01', '2014-06-01') \
    .filterBounds(ee.Geometry.Point(-122.092, 37.42))

# Load a secondary 'collection': GRIDMET meteorological data
gridmet = ee.ImageCollection('IDAHO_EPSCOR/GRIDMET')

# Define a max difference filter to compare timestamps.
maxDiffFilter = ee.Filter.maxDifference(**{
  'difference': 2 * 24 * 60 * 60 * 1000,
  'leftField': 'system:time_start',
  'rightField': 'system:time_start'
})

# Define the join.
saveBestJoin = ee.Join.saveBest(**{
  'matchKey': 'bestImage',
  'measureKey': 'timeDiff'
})

# Apply the join.
landsatMet = saveBestJoin.apply(primary, gridmet, maxDiffFilter)

# Print the result.
print(landsatMet.getInfo())

