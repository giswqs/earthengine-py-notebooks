import ee
from ee_plugin import Map
from ee_plugin.contrib import palettes

dem = ee.Image("JAXA/ALOS/AW3D30_V1_1").select('MED')
dem = dem.updateMask(dem.gt(0))
palette = palettes.cb['Pastel1'][7]
#palette = ['black', 'white']
rgb = dem.visualize(**{'min': 0, 'max': 5000, 'palette': palette })
hsv = rgb.unitScale(0, 255).rgbToHsv()

extrusion = 30
weight = 0.7

hs = ee.Terrain.hillshade(dem.multiply(extrusion), 315, 35).unitScale(10, 250).resample('bicubic')

hs = hs.multiply(weight).add(hsv.select('value').multiply(1 - weight))
hsv = hsv.addBands(hs.rename('value'), ['value'], True)
rgb = hsv.hsvToRgb()

Map.setCenter(0, 28, 2.5)
Map.addLayer(rgb, {}, 'ALOS DEM', True)
