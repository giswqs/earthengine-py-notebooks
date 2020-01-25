import ee 
from ee_plugin import Map 

# Define an arbitrary region in which to compute random points.
region = ee.Geometry.Rectangle(-119.224, 34.669, -99.536, 50.064)

# Create 1000 random points in the region.
randomPoints = ee.FeatureCollection.randomPoints(region)

# Display the points.
Map.centerObject(randomPoints)
Map.addLayer(randomPoints, {}, 'random points')
