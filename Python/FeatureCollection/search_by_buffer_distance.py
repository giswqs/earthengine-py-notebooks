# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/FeatureCollection/search_by_buffer_distance.py

#!/usr/bin/env python
"""FeatureCollection Join example.

Show parks in San Francisco within 2 kilometers of a BART station.
"""

import ee
from ee_plugin import Map

Map.setCenter(-122.45, 37.75, 13)

bart = ee.FeatureCollection('ft:1xCCZkVn8DIkB7i7RVkvsYWxAxsdsQZ6SbD9PCXw')
parks = ee.FeatureCollection('ft:10KC6VfBWMUvNcuxU7mbSEg__F_4UVe9uDkCldBw')
buffered_bart = bart.map(lambda f: f.buffer(2000))

join_filter = ee.Filter.withinDistance(2000, '.geo', None, '.geo')
close_parks = ee.Join.simple().apply(parks, bart, join_filter)

Map.addLayer(buffered_bart, {'color': 'b0b0b0'}, "BART Stations")
Map.addLayer(close_parks, {'color': '008000'}, "Parks")
