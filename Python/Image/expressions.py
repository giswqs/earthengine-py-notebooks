import ee 
from ee_plugin import Map 

# Load a Landsat 8 image.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')

# Compute the EVI using an expression.
evi = image.expression(
    '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
      'NIR': image.select('B5'),
      'RED': image.select('B4'),
      'BLUE': image.select('B2')
})

Map.centerObject(image, 9)
Map.addLayer(evi, {'min': -1, 'max': 1, 'palette': ['FF0000', '00FF00']}, "EVI")

