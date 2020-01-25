# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Image/image_patch_area.py

import ee 
from ee_plugin import Map 

geometry = ee.Geometry.Polygon(
        [[[-121.53162002563477, 37.62442917942242],
          [-121.53822898864746, 37.61871860390886],
          [-121.53307914733887, 37.61144378319061],
          [-121.5281867980957, 37.60784010375065],
          [-121.52209281921387, 37.60586820524277],
          [-121.51840209960938, 37.606344185530936],
          [-121.51273727416992, 37.60777210812061],
          [-121.50175094604492, 37.6082480762255],
          [-121.49454116821289, 37.61239566936059],
          [-121.49127960205078, 37.62136999709244],
          [-121.49797439575195, 37.62667249978579],
          [-121.5252685546875, 37.62653654290317]]])

# Load a Landsat 8 image and display the thermal band.
image = ee.Image('LANDSAT/LC8_L1T_TOA/LC80440342014077LGN00').clip(geometry)
Map.setCenter(-121.51385307312012,37.61767615130697, 14) # SF Bay
#Map.addLayer(image, {'bands': ['B10'], 'min': 270, 'max': 310}, 'LST')
#print(image)

# Threshold the thermal band to find "hot" objects.
hotspots = image.select('B10').gt(303)

# Mask "cold" pixels.
hotspots = hotspots.mask(hotspots)
#Map.addLayer(hotspots, {'palette': 'FF0000'}, 'hotspots')

# Compute the number of pixels in each patch.
patchsize = hotspots.connectedPixelCount(100, False)
Map.addLayer(patchsize, {}, 'patch size')
largePatches = patchsize.gt(4)
largePatches = largePatches.updateMask(largePatches)
Map.addLayer(largePatches, {}, 'patch size>4')

pixelAreaAllPatches = hotspots.multiply(ee.Image.pixelArea())
pixelAreaLargePatch = largePatches.multiply(ee.Image.pixelArea())
areaAllPathces = pixelAreaAllPatches.reduceRegion(**{'reducer':ee.Reducer.sum(),'geometry':geometry})
areaLargePatch = pixelAreaLargePatch.reduceRegion(**{'reducer':ee.Reducer.sum(),'geometry':geometry})

print(areaAllPathces.getInfo())
print(areaLargePatch.getInfo())