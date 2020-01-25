import ee
from ee_plugin import Map

image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')
centroid = image.geometry().centroid().coordinates()
lon = centroid.get(0).getInfo()
lat = centroid.get(1).getInfo()

# Create an NDWI image, define visualization parameters and display.
ndwi = image.normalizedDifference(['B3', 'B5'])
ndwiViz = {'min': 0.5, 'max': 1, 'palette': ['00FFFF', '0000FF']}

# Mask the non-watery parts of the image, where NDWI < 0.4.
ndwiMasked = ndwi.updateMask(ndwi.gte(0.4))

# Create visualization layers.
imageRGB = image.visualize(**{'bands': ['B5', 'B4', 'B3'], 'max': 0.5})
ndwiRGB = ndwiMasked.visualize(**{
  'min': 0.5,
  'max': 1,
  'palette': ['00FFFF', '0000FF']
})

# Mosaic the visualization layers and display (or export).
mosaic = ee.ImageCollection([imageRGB, ndwiRGB]).mosaic()
Map.setCenter(lon, lat, 10)
Map.addLayer(mosaic, {}, 'mosaic', False)

# Create a circle by drawing a 20000 meter buffer around a point.
roi = ee.Geometry.Point([-122.4481, 37.7599]).buffer(20000)

# Display a clipped version of the mosaic.
Map.addLayer(mosaic.clip(roi), {}, "roi")