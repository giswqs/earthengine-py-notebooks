import ee
from ee_plugin import Map

image = ee.Image('LANDSAT/LC8_L1T_TOA/LC80440342014077LGN00')

roi = ee.Geometry.Point([-122.4481, 37.7599]).buffer(20000)

clipped = image.clip(roi)

# print(image.getInfo())
Map.setCenter(-122.1899, 37.5010, 10)
vis = {'bands': ['B5', 'B4', 'B3'], 'min': 0, 'max': 0.5, 'gamma': [0.95, 1.1, 1]}
Map.addLayer(image, vis, "Full Image", False)
Map.addLayer(clipped, vis, "Clipped Image")
