import ee 
from ee_plugin import Map 

# Create a FeatureCollection from an Earth Engine Table.

# Load census roads.
roads = ee.FeatureCollection('TIGER/2016/Roads')

# Get only interstates.
interstates = roads.filter(ee.Filter.eq('rttyp', 'I'))

# Get only surface roads.
surfaceRoads = roads.filter(ee.Filter.eq('rttyp', 'M'))

# Display the roads in different colors.
Map.addLayer(surfaceRoads, {'color': 'gray'}, 'surface roads')
Map.addLayer(interstates, {'color': 'red'}, 'interstates')

