import ee
from ee_plugin import Map

# Load an image.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')
centroid = image.geometry().centroid().coordinates()
lon = centroid.get(0).getInfo()
lat = centroid.get(1).getInfo()
# print(centroid.getInfo())

# Create an NDWI image, define visualization parameters and display.
ndwi = image.normalizedDifference(['B3', 'B5'])
ndwiViz = {'min': 0.5, 'max': 1, 'palette': ['00FFFF', '0000FF']}

# Mask the non-watery parts of the image, where NDWI < 0.4.
ndwiMasked = ndwi.updateMask(ndwi.gte(0.4))

Map.setCenter(lon, lat, 10)
Map.addLayer(ndwi, ndwiViz, 'NDWI', False)
Map.addLayer(ndwiMasked, ndwiViz, 'NDWI masked')
