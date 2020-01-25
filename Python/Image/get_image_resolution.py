# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Image/get_image_resolution.py

import ee 
from ee_plugin import Map 

naip = ee.Image('USDA/NAIP/DOQQ/m_3712213_sw_10_1_20140613')
Map.setCenter(-122.466123, 37.769833, 17)
Map.addLayer(naip, {'bands': ['N', 'R','G']}, 'NAIP')

naip_resolution =naip.select('N').projection().nominalScale()
print("NAIP resolution: ", naip_resolution.getInfo())


landsat = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318')
landsat_resolution =landsat.select('B1').projection().nominalScale()
print("Landsat resolution: ", landsat_resolution.getInfo())