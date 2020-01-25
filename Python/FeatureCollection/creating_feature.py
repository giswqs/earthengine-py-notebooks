import ee 
from ee_plugin import Map 

# Create an ee.Geometry.
polygon = ee.Geometry.Polygon([
  [[-35, -10], [35, -10], [35, 10], [-35, 10], [-35, -10]]
])

# Create a Feature from the Geometry.
polyFeature = ee.Feature(polygon, {'foo': 42, 'bar': 'tart'})


print(polyFeature.getInfo())
Map.addLayer(polyFeature, {}, 'feature')

