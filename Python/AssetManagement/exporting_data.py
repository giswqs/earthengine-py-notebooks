import ee
from ee_plugin import Map



image = ee.Image('USDA/NAIP/DOQQ/m_4609915_sw_14_1_20100629')

# downConfig = {'scale':30, "maxPixels": 1.0E13, 'driveFolder':'test', 'CRS': 'EPGS:31983', 'region': roiExample }
#
# task = ee.batch.Export.image(image.select( ['B2', 'B3' ,'B4', 'B5',  'B6']).toDouble(), 'sirgas20023sPy', downConfig)
# task.start()

downConfig = {'scale': 10, "maxPixels": 1.0E13, 'driveFolder': 'image'}  # scale means resolution.
task = ee.batch.Export.image(image, "10m", downConfig)
task.start()