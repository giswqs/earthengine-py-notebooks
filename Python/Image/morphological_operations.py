import ee 
from ee_plugin import Map 

# Load a Landsat 8 image, select the NIR band, threshold, display.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318') \
            .select(4).gt(0.2)
Map.setCenter(-122.1899, 37.5010, 13)
Map.addLayer(image, {}, 'NIR threshold')

# Define a kernel.
kernel = ee.Kernel.circle(**{'radius': 1})

# Perform an erosion followed by a dilation, display.
opened = image \
             .focal_min(**{'kernel': kernel, 'iterations': 2}) \
             .focal_max(**{'kernel': kernel, 'iterations': 2})
Map.addLayer(opened, {}, 'opened')

