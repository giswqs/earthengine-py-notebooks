# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Image/download.py

#!/usr/bin/env python
"""Download example."""

import ee
from ee_plugin import Map

# Get a download URL for an image.
image1 = ee.Image('srtm90_v4')
path = image1.getDownloadUrl({
    'scale': 30,
    'crs': 'EPSG:4326',
    'region': '[[-120, 35], [-119, 35], [-119, 34], [-120, 34]]'
})

print(path)
vis_params = {'min': 0, 'max': 3000}
Map.addLayer(image1, vis_params)
