import ee 
from ee_plugin import Map 

# Load a Landsat 8 image.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')

# Create NDVI and NDWI spectral indices.
ndvi = image.normalizedDifference(['B5', 'B4'])
ndwi = image.normalizedDifference(['B3', 'B5'])

# Create a binary layer using logical operations.
bare = ndvi.lt(0.2).And(ndwi.lt(0))

# Mask and display the binary layer.
Map.setCenter(-122.3578, 37.7726, 12)
Map.setOptions('satellite')
Map.addLayer(bare.updateMask(bare), {}, 'bare')

