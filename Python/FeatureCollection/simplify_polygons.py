# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/FeatureCollection/simplify_polygons.py

import ee 
from ee_plugin import Map 

waterSurface = ee.Image('JRC/GSW1_0/GlobalSurfaceWater')
waterChange = waterSurface.select('transition')
 # Select Permanent Water Only:
Permanent_Water = 1 # value 1 represents pixels of permenant water, no change
waterMask = waterChange.eq(Permanent_Water) # Water mask boolean = 1 to detect whater bodies
# Map.setCenter(24.43874, 61.58173, 10)
# Map.addLayer(waterMask, {}, 'Water Mask')
# Map.centerObject(masked)
OnlyLakes = waterMask.updateMask(waterMask)

roi = ee.Geometry.Polygon(
        [[[22.049560546875, 61.171214253920965],
          [22.0330810546875, 60.833021871926185],
          [22.57415771484375, 60.83168327936567],
          [22.5714111328125, 61.171214253920965]]])

classes = OnlyLakes.reduceToVectors(**{
  'reducer': ee.Reducer.countEvery(),
  'geometry': roi,
  'scale': 30,
  'maxPixels': 1e10
})
simpleClasses = classes.geometry().simplify(50)

Map.centerObject(ee.FeatureCollection(roi), 10)
Map.addLayer(ee.Image().paint(classes, 0, 2),{'palette': 'red'}, "original")
Map.addLayer(ee.Image().paint(simpleClasses, 0, 2),{'palette': 'blue'}, "simplified")
