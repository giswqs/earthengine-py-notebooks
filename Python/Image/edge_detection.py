import ee 
from ee_plugin import Map 

# Load a Landsat 8 image, select the panchromatic band.
image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318').select('B8')

# Perform Canny edge detection and display the result.
canny = ee.Algorithms.CannyEdgeDetector(**{
  'image': image, 'threshold': 10, 'sigma': 1
})
Map.setCenter(-122.054, 37.7295, 10)
Map.addLayer(canny, {}, 'canny')

# Perform Hough transform of the Canny result and display.
hough = ee.Algorithms.HoughTransform(canny, 256, 600, 100)
Map.addLayer(hough, {}, 'hough')

# Load a Landsat 8 image, select the panchromatic band.
image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318').select('B8')
Map.addLayer(image, {'max': 12000})

# Define a "fat" Gaussian kernel.
fat = ee.Kernel.gaussian(**{
  'radius': 3,
  'sigma': 3,
  'units': 'pixels',
  'normalize': True,
  'magnitude': -1
})

# Define a "skinny" Gaussian kernel.
skinny = ee.Kernel.gaussian(**{
  'radius': 3,
  'sigma': 1,
  'units': 'pixels',
  'normalize': True,
})

# Compute a difference-of-Gaussians (DOG) kernel.
dog = fat.add(skinny)

# Compute the zero crossings of the second derivative, display.
zeroXings = image.convolve(dog).zeroCrossing()
Map.setCenter(-122.054, 37.7295, 10)
Map.addLayer(zeroXings.updateMask(zeroXings), {'palette': 'FF0000'}, 'zero crossings')

