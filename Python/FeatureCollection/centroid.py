import ee 
from ee_plugin import Map 

# Create a geodesic polygon.
polygon = ee.Geometry.Polygon([
  [[-5, 40], [65, 40], [65, 60], [-5, 60], [-5, 60]]
])

# Compute a buffer of the polygon.
buffer = polygon.buffer(0.1)

# Compute the centroid of the polygon.
centroid = polygon.centroid()
Map.addLayer(buffer, {}, 'buffer')
Map.addLayer(centroid, {'color': 'red'}, 'centroid')

