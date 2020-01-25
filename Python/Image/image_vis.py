import ee
from ee_plugin import Map

image = ee.Image('LANDSAT/LC8_L1T_TOA/LC80440342014077LGN00')
# print(image.getInfo())
Map.setCenter(-122.1899, 37.5010, 10)
vis = {'bands': ['B5', 'B4', 'B3'], 'min': 0, 'max': 0.5, 'gamma': [0.95, 1.1, 1]}
# Map.addLayer(image, vis)


# Color palettes
image = ee.Image('LANDSAT/LC8_L1T_TOA/LC80440342014077LGN00')
ndwi = image.normalizedDifference(['B3', 'B5'])
ndwiViz = {'min': 0.5, 'max': 1, 'palette': ['00FFFF', '0000FF']}
# Map.addLayer(ndwi, ndwiViz, 'NDWI')

# Masking
ndwiMasked = ndwi.updateMask(ndwi.gte(0.4))
# Map.addLayer(ndwiMasked, ndwiViz, 'NDWI masked')

# Create visualization layers.
imageRGB = image.visualize({'bands': ['B5', 'B4', 'B3'], max: 0.5})
ndwiRGB = ndwiMasked.visualize({
    'min': 0.5,
    'max': 1,
    'palette': ['00FFFF', '0000FF']
})

# Mosaic the visualization layers and display( or export).
# mosaic = ee.ImageCollection([imageRGB, ndwiRGB]).mosaic()
# mosaic = ee.ImageCollection([image,ndwiMasked]).mosaic()
# Map.addLayer(mosaic, {}, 'mosaic')


roi = ee.Geometry.Point([-122.4481, 37.7599]).buffer(20000)
Map.addLayer(image.clip(roi), vis, 'Landsat 8')
Map.addLayer(ndwiMasked.clip(roi),ndwiViz, 'NDWI')

