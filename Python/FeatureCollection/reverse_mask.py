#!/usr/bin/env python
"""Reverse mask a region.

Create an image that masks everything except for the specified polygon.
"""

import ee
from ee_plugin import Map

Map.setCenter(-100, 40, 4)

fc = (ee.FeatureCollection('ft:1Ec8IWsP8asxN-ywSqgXWMuBaxI6pPaeh6hC64lA')
      .filter(ee.Filter().eq('ECO_NAME', 'Great Basin shrub steppe')))

# Start with a black image.
empty = ee.Image(0).toByte()
# Fill and outline the polygons in two colors
filled = empty.paint(fc, 2)
both = filled.paint(fc, 1, 5)
# Mask off everything that matches the fill color.
result = both.mask(filled.neq(2))

Map.addLayer(result, {
    'palette': '000000,FF0000',
    'max': 1,
    'opacity': 0.5
}, "Basin")
