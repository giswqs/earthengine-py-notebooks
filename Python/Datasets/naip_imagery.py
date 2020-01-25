import ee
from ee_plugin import Map
image = ee.Image('USDA/NAIP/DOQQ/m_4609915_sw_14_1_20100629')
Map.addLayer(image, {'bands': ['N', 'R', 'G']}, 'NAIP')