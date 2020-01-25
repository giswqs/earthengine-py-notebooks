#!/usr/bin/env python
"""Composite an image collection and clip it to a boundary from a fusion table.

See also: Filtered Seasonal Composite, which filters the
collection by bounds instead.
"""

# import datetime
import ee
from ee_plugin import Map


Map.setCenter(-110, 40, 5)
fc = ee.FeatureCollection('TIGER/2018/States').filter(ee.Filter.eq('STUSPS', 'MN'))

# Create a Landsat 7, median-pixel composite for Spring of 2000.
collection = ee.ImageCollection('LE7_L1T').filterDate("2000-05-01", "2000-10-31") \
      .filterBounds(fc)
image1 = collection.median()
# Map.addLayer(image1)

# # Clip to the output image to the California state boundary.
# # fc = (ee.FeatureCollection('ft:1fRY18cjsHzDgGiJiS2nnpUU3v9JPDc2HNaR7Xk8')
# #       .filter(ee.Filter().eq('Name', 'Minnesota')))


image2 = image1.clipToCollection(fc)

# Select the red, green and blue bands.
image = image2.select('B4', 'B3', 'B2')
Map.addLayer(image, {'gain': [1.4, 1.4, 1.1]}, 'Landsat 7')
