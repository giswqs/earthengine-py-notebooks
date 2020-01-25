#!/usr/bin/env python
"""Count features example.

Count Panoramio photos near SF that mention bridges.
"""

import ee
from ee_plugin import Map


Map.setCenter(-122.39, 37.7857, 12)

photos_near_sf = ee.FeatureCollection(
    'ft:1qpKIcYQMBsXLA9RLWCaV9D0Hus2cMQHhI-ViKHo')
bridge_photos = photos_near_sf.filter(
    ee.Filter().Or(ee.Filter.stringContains('title', 'Bridge'),
                   ee.Filter.stringContains('title', 'bridge')))

Map.addLayer(photos_near_sf, {'color': '0040b0'}, "Photos near SF")
Map.addLayer(bridge_photos, {'color': 'e02070'}, "Bridge photos")

print ('There are %d bridge photos around SF.' %
       bridge_photos.size().getInfo())
