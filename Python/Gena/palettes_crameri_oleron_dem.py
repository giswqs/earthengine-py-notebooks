import ee
from ee_plugin import Map
from ee_plugin.contrib import palettes

dem = ee.Image("AHN/AHN2_05M_RUW").convolve(ee.Kernel.gaussian(0.5, 0.3, 'meters'))

extrusion = 3
weight = 0.7
palette = palettes.crameri['oleron'][50]

rgb = dem.visualize(**{'min': 0, 'max': 3, 'palette': palette })
hsv = rgb.unitScale(0, 255).rgbToHsv()
hs = ee.Terrain.hillshade(dem.multiply(extrusion), 315, 35).unitScale(0, 255)
hs = hs.multiply(weight).add(hsv.select('value').multiply(1 - weight))
saturation = hsv.select('saturation').multiply(0.5)
hsv = hsv.addBands(hs.rename('value'), ['value'], True)
hsv = hsv.addBands(saturation, ['saturation'], True)
rgb = hsv.hsvToRgb()

# rgb = rgb.updateMask(dem.unitScale(0, 3))

Map.addLayer(rgb, {}, 'Dutch AHN DEM', True)
Map.setCenter(4.5618, 52.1664, 18)
