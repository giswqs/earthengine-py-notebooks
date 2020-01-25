import ee 
from ee_plugin import Map 

# Load an image and select some bands of interest.
image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318') \
    .select(['B4', 'B3', 'B2'])

# Reduce the image to get a one-band maximum value image.
maxValue = image.reduce(ee.Reducer.max())

# Display the result.
Map.centerObject(image, 10)
Map.addLayer(maxValue, {'max': 13000}, 'Maximum value image')

