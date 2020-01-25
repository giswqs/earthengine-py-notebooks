#!/usr/bin/env python
"""Computed area filter example.

Find US counties smaller than 3k square kilometers in area.
"""

import ee
from ee_plugin import Map


Map.setCenter(-119.7, 38.26, 7)

# counties = ee.FeatureCollection(
#     'ft:1pjtcfSKIbYbj4wRcBjc0Bb6NB-sQRI-L2nIzHiU')
counties = ee.FeatureCollection("TIGER/2016/Counties")
counties_with_area = counties.map(lambda f: f.set({'area': f.area()}))
small_counties = counties_with_area.filterMetadata('area', 'less_than', 3e9)

Map.addLayer(small_counties, {'color': '900000'}, "Small US counties")
