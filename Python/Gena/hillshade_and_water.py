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

Map.addLayer(rgb, {}, 'ALOS DEM', True, 0.5)

water_occurrence = ( ee.Image("JRC/GSW1_0/GlobalSurfaceWater")
  .select('occurrence')
  .divide(100)
  .unmask(0)
  .resample('bicubic') )
  
palette = ["ffffcc","ffeda0","fed976","feb24c","fd8d3c","fc4e2a","e31a1c","bd0026","800026"][::-1][1:]

land = ee.Image("users/gena/land_polygons_image").mask()

Map.addLayer(water_occurrence.mask(water_occurrence.multiply(2).multiply(land)), {'min': 0, 'max': 1, 'palette': palette}, 'water occurrence', True)




