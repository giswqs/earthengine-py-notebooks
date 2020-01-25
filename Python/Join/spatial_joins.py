import ee 
from ee_plugin import Map 

# Load a primary 'collection': protected areas (Yosemite National Park).
primary = ee.FeatureCollection("WCMC/WDPA/current/polygons") \
  .filter(ee.Filter.eq('NAME', 'Yosemite National Park'))

# Load a secondary 'collection': power plants.
powerPlants = ee.FeatureCollection('WRI/GPPD/power_plants')

# Define a spatial filter, with distance 100 km.
distFilter = ee.Filter.withinDistance(**{
  'distance': 100000,
  'leftField': '.geo',
  'rightField': '.geo',
  'maxError': 10
})

# Define a saveAll join.
distSaveAll = ee.Join.saveAll(**{
  'matchesKey': 'points',
  'measureKey': 'distance'
})

# Apply the join.
spatialJoined = distSaveAll.apply(primary, powerPlants, distFilter)

# Print the result.
# print(spatialJoined.getInfo())
Map.centerObject(spatialJoined, 10)
Map.addLayer(ee.Image().paint(spatialJoined, 1, 3), {}, 'Spatial Joined')
