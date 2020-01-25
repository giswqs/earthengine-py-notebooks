import ee 
from ee_plugin import Map 

# Load and display an image.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')
Map.setCenter(-121.9785, 37.8694, 11)
Map.addLayer(image, {'bands': ['B5', 'B4', 'B3'], 'max': 0.5}, 'input image')

# Define a boxcar or low-pass kernel.
# boxcar = ee.Kernel.square({
#   'radius': 7, 'units': 'pixels', 'normalize': True
# })

boxcar = ee.Kernel.square(7, 'pixels', True)

# Smooth the image by convolving with the boxcar kernel.
smooth = image.convolve(boxcar)
Map.addLayer(smooth, {'bands': ['B5', 'B4', 'B3'], 'max': 0.5}, 'smoothed')

# Define a Laplacian, or edge-detection kernel.
laplacian = ee.Kernel.laplacian8(1, False)

# Apply the edge-detection kernel.
edgy = image.convolve(laplacian)
Map.addLayer(edgy,
             {'bands': ['B5', 'B4', 'B3'], 'max': 0.5},
             'edges')

