import ee 
from ee_plugin import Map 

# Load a Landsat 5 image and select the bands we want to unmix.
bands = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']
image = ee.Image('LANDSAT/LT05/C01/T1/LT05_044034_20080214') \
  .select(bands)
Map.setCenter(-122.1899, 37.5010, 10) # San Francisco Bay
Map.addLayer(image, {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 128}, 'image')

# Define spectral endmembers.
urban = [88, 42, 48, 38, 86, 115, 59]
veg = [50, 21, 20, 35, 50, 110, 23]
water = [51, 20, 14, 9, 7, 116, 4]

# Unmix the image.
fractions = image.unmix([urban, veg, water])
Map.addLayer(fractions, {}, 'unmixed')

