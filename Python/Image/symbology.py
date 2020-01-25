import ee
from ee_plugin import Map


cover = ee.Image('MODIS/051/MCD12Q1/2012_01_01').select('Land_Cover_Type_1')

igbpPalette = [
    'aec3d4',
    '152106', '225129', '369b47', '30eb5b', '387242',
    '6a2325', 'c3aa69', 'b76031', 'd9903d', '91af40',
    '111149',
    'cdb33b',
    'cc0013',
    '33280d',
    'd7cdcc',
    'f7e084',
    '6f6f6f'
]

Map.setCenter(-99.229, 40.413, 5)
Map.addLayer(cover, {'min': 0, 'max': 17, 'palette': igbpPalette}, 'MODIS Land Cover')

