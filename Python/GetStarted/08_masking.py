import ee
from ee_plugin import Map

# This function gets NDVI from Landsat 5 imagery.


def getNDVI(image):
    return image.normalizedDifference(['B4', 'B3'])


# Load two Landsat 5 images, 20 years apart.
image1 = ee.Image('LANDSAT/LT05/C01/T1_TOA/LT05_044034_19900604')
image2 = ee.Image('LANDSAT/LT05/C01/T1_TOA/LT05_044034_20100611')

# Compute NDVI from the scenes.
ndvi1 = getNDVI(image1)
ndvi2 = getNDVI(image2)

# Compute the difference in NDVI.
ndviDifference = ndvi2.subtract(ndvi1)
# Load the land mask from the SRTM DEM.
landMask = ee.Image('CGIAR/SRTM90_V4').mask()

# Update the NDVI difference mask with the land mask.
maskedDifference = ndviDifference.updateMask(landMask)

# Display the masked result.
vizParams = {'min': -0.5, 'max': 0.5,
             'palette': ['FF0000', 'FFFFFF', '0000FF']}
Map.setCenter(-122.2531, 37.6295, 9)
Map.addLayer(maskedDifference, vizParams, 'NDVI difference')
