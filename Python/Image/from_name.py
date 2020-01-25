#!/usr/bin/env python
"""Display an image given its ID."""

import ee
from ee_plugin import Map

image = ee.Image('srtm90_v4')
vis_params = {'min': 0, 'max': 3000}
Map.addLayer(image, vis_params,"SRTM")
Map.setCenter(0,0, 2)
