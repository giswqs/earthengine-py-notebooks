import ee 
import math
from ee_plugin import Map 

# Load a high-resolution NAIP image.
image = ee.Image('USDA/NAIP/DOQQ/m_3712213_sw_10_1_20140613')

# Zoom to San Francisco, display.
Map.setCenter(-122.466123, 37.769833, 17)
Map.addLayer(image, {'max': 255}, 'image')

# Get the NIR band.
nir = image.select('N')

# Define a neighborhood with a kernel.
square = ee.Kernel.square(**{'radius': 4})

# Compute entropy and display.
entropy = nir.entropy(square)
Map.addLayer(entropy,
             {'min': 1, 'max': 5, 'palette': ['0000CC', 'CC0000']},
             'entropy')

# Compute the gray-level co-occurrence matrix (GLCM), get contrast.
glcm = nir.glcmTexture(**{'size': 4})
contrast = glcm.select('N_contrast')
Map.addLayer(contrast,
             {'min': 0, 'max': 1500, 'palette': ['0000CC', 'CC0000']},
             'contrast')

# Create a list of weights for a 9x9 kernel.
list = [1, 1, 1, 1, 1, 1, 1, 1, 1]
# The center of the kernel is zero.
centerList = [1, 1, 1, 1, 0, 1, 1, 1, 1]
# Assemble a list of lists: the 9x9 kernel weights as a 2-D matrix.
lists = [list, list, list, list, centerList, list, list, list, list]
# Create the kernel from the weights.
# Non-zero weights represent the spatial neighborhood.
kernel = ee.Kernel.fixed(9, 9, lists, -4, -4, False)

# Convert the neighborhood into multiple bands.
neighs = nir.neighborhoodToBands(kernel)

# Compute local Geary's C, a measure of spatial association.
gearys = nir.subtract(neighs).pow(2).reduce(ee.Reducer.sum()) \
             .divide(math.pow(9, 2))
Map.addLayer(gearys,
             {'min': 20, 'max': 2500, 'palette': ['0000CC', 'CC0000']},
             "Geary's C")

