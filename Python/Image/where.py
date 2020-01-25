#!/usr/bin/env python
"""Where operator example.

Select the forest classes from the MODIS land cover image and intersect them
with elevations above 1000m.
"""

import ee
from ee_plugin import Map

Map.setCenter(-113.41842, 40.055489, 6)

elev = ee.Image('srtm90_v4')
cover = ee.Image('MCD12Q1/MCD12Q1_005_2001_01_01').select('Land_Cover_Type_1')
blank = ee.Image(0)

# Where (1 <= cover <= 4) and (elev > 1000), set the output to 1.
output = blank.where(
    cover.lte(4).And(cover.gte(1)).And(elev.gt(1000)),
    1)

# Output contains 0s and 1s.  Mask it with itself to get rid of the 0s.
result = output.mask(output)
vis = {'min': 0, 'max': 3000}
Map.addLayer(elev, vis, 'SRTM')
Map.addLayer(result, {'palette': '00AA00'}, 'Land Cover')
