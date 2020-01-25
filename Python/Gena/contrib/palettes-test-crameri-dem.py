import ee

from ee_plugin import Map
from ee_plugin.contrib import utils, palettes

Map.setCenter(4.408241, 52.177595, 18)

dem = ee.Image("AHN/AHN2_05M_RUW") \
  .resample('bicubic') \
  .convolve(ee.Kernel.gaussian(0.5, 0.25, 'meters'))

#  palette = palettes.crameri['lisbon'][50]
palette = palettes.crameri['oleron'][50]
#  palette = palettes.crameri['roma'][50].slice(0).reverse()

demRGB = dem.visualize(**{ 'min': -5, 'max': 15, 'palette': palette })

weight = 0.4 # wegith of Hillshade vs RGB intensity (0 - flat, 1 - HS)
exaggeration = 5 # vertical exaggeration
azimuth = 315 # Sun azimuth
zenith = 20 # Sun elevation
brightness = -0.05 # 0 - default
contrast = 0.05 # 0 - default
saturation = 0.8 # 1 - default
castShadows = False

# no shadows
rgb = utils.hillshadeRGB(demRGB, dem, weight, exaggeration, azimuth, zenith, contrast, brightness, saturation, castShadows)
Map.addLayer(rgb, {}, 'DEM (no shadows)', False)

# with shadows
castShadows = True
rgb = utils.hillshadeRGB(demRGB, dem, weight, exaggeration, azimuth, zenith, contrast, brightness, saturation, castShadows)
Map.addLayer(rgb, {}, 'DEM')

Map.addLayer(dem, {}, 'DEM (raw)', False)
