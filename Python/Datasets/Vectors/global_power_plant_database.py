# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Datasets/Vectors/global_power_plant_database.py

import ee 
from ee_plugin import Map 

# Visualization for WRI/GPPD/power_plants
# https:#code.earthengine.google.com/9efbd726e4a8ba9b8b56ba94f1267678

table = ee.FeatureCollection("WRI/GPPD/power_plants")

# Get a color from a fuel
fuelColor = ee.Dictionary({
  'Coal': '000000',
  'Oil': '593704',
  'Gas': 'BC80BD',
  'Hydro': '0565A6',
  'Nuclear': 'E31A1C',
  'Solar': 'FF7F00',
  'Waste': '6A3D9A',
  'Wind': '5CA2D1',
  'Geothermal': 'FDBF6F',
  'Biomass': '229A00'
})

# List of fuels to add to the map
fuels = ['Coal', 'Oil', 'Gas', 'Hydro', 'Nuclear', 'Solar', 'Waste',
    'Wind', 'Geothermal', 'Biomass']

# /**
#  * Computes size from capacity and color from fuel type.
#  *
#  * @param {!ee.Geometry.Point} pt A point
#  * @return {!ee.Geometry.Point} Input point with added style dictionary.
#  */
def addStyle(pt):
  size = ee.Number(pt.get('capacitymw')).sqrt().divide(10).add(2)
  color = fuelColor.get(pt.get('fuel1'))
  return pt.set('styleProperty', ee.Dictionary({'pointSize': size, 'color': color}))


# Make a FeatureCollection out of the power plant data table
pp = ee.FeatureCollection(table).map(addStyle)
# print(pp.first())

# /**
#  * Adds power plants of a certain fuel type to the map.
#  *
#  * @param {string} fuel A fuel type
#  */
def addLayer(fuel):
#   print(fuel)
  Map.addLayer(pp.filter(ee.Filter.eq('fuel1', fuel)).style({'styleProperty': 'styleProperty', 'neighborhood': 50}), {}, fuel, True, 0.65)


# Apply `addLayer` to each record in `fuels`
for fuel in fuels:
    Map.addLayer(pp.filter(ee.Filter.eq('fuel1', fuel)).style(**{'styleProperty': 'styleProperty', 'neighborhood': 50}), {}, fuel, True, 0.65)
