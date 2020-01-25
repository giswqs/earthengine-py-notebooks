import ee 
from ee_plugin import Map 

def intersect(state):
  nPowerPlants = ee.List(state.get('power_plants')).size()
  # Return the state feature with a new property: power plant count.
  return state.set('n_power_plants', nPowerPlants)

# Load the primary 'collection': US state boundaries.
states = ee.FeatureCollection('TIGER/2018/States')

# Load the secondary 'collection': power plants.
powerPlants = ee.FeatureCollection('WRI/GPPD/power_plants')

# Define a spatial filter as geometries that intersect.
spatialFilter = ee.Filter.intersects(**{
  'leftField': '.geo',
  'rightField': '.geo',
  'maxError': 10
})

# Define a save all join.
saveAllJoin = ee.Join.saveAll(**{
  'matchesKey': 'power_plants',
})

# Apply the join.
intersectJoined = saveAllJoin.apply(states, powerPlants, spatialFilter)

# Add power plant count per state as a property.
intersectJoined = intersectJoined.map(intersect)
# intersectJoined = intersectJoined.map(function(state) {
#   # Get "power_plant" intersection list, count how many intersected this state.
#   nPowerPlants = ee.List(state.get('power_plants')).size()
#   # Return the state feature with a new property: power plant count.
#   return state.set('n_power_plants', nPowerPlants)
# })

print(intersectJoined.getInfo())

# # Make a bar chart for the number of power plants per state.
# chart = ui.Chart.feature.byFeature(intersectJoined, 'NAME', 'n_power_plants') \
#   .setChartType('ColumnChart') \
#   .setSeriesNames({n_power_plants: 'Power plants'}) \
#   .setOptions({
#     title: 'Power plants per state',
#     hAxis: {title: 'State'},
#     vAxis: {title: 'Frequency'}})

# # Print the chart to the console.
# print(chart)
