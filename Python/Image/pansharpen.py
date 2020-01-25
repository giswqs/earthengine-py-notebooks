import ee 
from ee_plugin import Map 

# Load a Landsat 8 top-of-atmosphere reflectance image.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')
Map.addLayer(
    image,
    {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 0.25, 'gamma': [1.1, 1.1, 1]},
    'rgb')

# Convert the RGB bands to the HSV color space.
hsv = image.select(['B4', 'B3', 'B2']).rgbToHsv()

# Swap in the panchromatic band and convert back to RGB.
sharpened = ee.Image.cat([
  hsv.select('hue'), hsv.select('saturation'), image.select('B8')
]).hsvToRgb()

# Display the pan-sharpened result.
Map.setCenter(-122.44829, 37.76664, 13)
Map.addLayer(sharpened,
             {'min': 0, 'max': 0.25, 'gamma': [1.3, 1.3, 1.3]},
             'pan-sharpened')

