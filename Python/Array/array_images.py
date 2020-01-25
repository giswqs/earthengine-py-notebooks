import ee 
from ee_plugin import Map 

# Define an Array of Tasseled Cap coefficients.
coefficients = ee.Array([
  [0.3037, 0.2793, 0.4743, 0.5585, 0.5082, 0.1863],
  [-0.2848, -0.2435, -0.5436, 0.7243, 0.0840, -0.1800],
  [0.1509, 0.1973, 0.3279, 0.3406, -0.7112, -0.4572],
  [-0.8242, 0.0849, 0.4392, -0.0580, 0.2012, -0.2768],
  [-0.3280, 0.0549, 0.1075, 0.1855, -0.4357, 0.8085],
  [0.1084, -0.9022, 0.4120, 0.0573, -0.0251, 0.0238]
])

# Load a Landsat 5 image, select the bands of interest.
image = ee.Image('LANDSAT/LT05/C01/T1_TOA/LT05_044034_20081011') \
  .select(['B1', 'B2', 'B3', 'B4', 'B5', 'B7'])

# Make an Array Image, with a 1-D Array per pixel.
arrayImage1D = image.toArray()

# Make an Array Image with a 2-D Array per pixel, 6x1.
arrayImage2D = arrayImage1D.toArray(1)

# Do a matrix multiplication: 6x6 times 6x1.
componentsImage = ee.Image(coefficients) \
  .matrixMultiply(arrayImage2D) \
  .arrayProject([0]) \
  .arrayFlatten(
    [['brightness', 'greenness', 'wetness', 'fourth', 'fifth', 'sixth']])

# Display the first three bands of the result and the input imagery.
vizParams = {
  'bands': ['brightness', 'greenness', 'wetness'],
  'min': -0.1, 'max': [0.5, 0.1, 0.1]
}
Map.setCenter(-122.3, 37.562, 10)
Map.addLayer(image, {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 0.5}, 'image')
Map.addLayer(componentsImage, vizParams, 'components')

