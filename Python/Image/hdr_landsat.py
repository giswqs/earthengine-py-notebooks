#!/usr/bin/env python
"""HDR Landsat.

Display portions of an image with different dynamic ranges.
The land areas are displayed normally, but the water areas
are streched to show more details.
"""

import datetime
import ee
from ee_plugin import Map


Map.setCenter(-95.738, 18.453, 9)

# Filter the LE7 collection to a single date.
collection = (ee.ImageCollection('LE7_L1T')
              .filterDate(datetime.datetime(2002, 11, 8),
                          datetime.datetime(2002, 11, 9)))
image = collection.mosaic().select('B3', 'B2', 'B1')

# Display the image normally.
Map.addLayer(image, {'gain': '1.6, 1.4, 1.1'}, 'Land')

# Add and stretch the water.  Once where the elevation is masked,
# and again where the elevation is zero.
elev = ee.Image('srtm90_v4')
mask1 = elev.mask().eq(0).And(image.mask())
mask2 = elev.eq(0).And(image.mask())
Map.addLayer(image.mask(mask1), {'gain': 6.0, 'bias': -200}, 'Water: Masked')
Map.addLayer(image.mask(mask2), {'gain': 6.0, 'bias': -200}, 'Water: Elev 0')
