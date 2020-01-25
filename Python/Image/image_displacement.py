import ee 
import math
from ee_plugin import Map 

# Load the two images to be registered.
image1 = ee.Image('SKYSAT/GEN-A/PUBLIC/ORTHO/MULTISPECTRAL/s01_20150502T082736Z')
image2 = ee.Image('SKYSAT/GEN-A/PUBLIC/ORTHO/MULTISPECTRAL/s01_20150305T081019Z')

# Use bicubic resampling during registration.
image1Orig = image1.resample('bicubic')
image2Orig = image2.resample('bicubic')

# Choose to register using only the 'R' bAnd.
image1RedBAnd = image1Orig.select('R')
image2RedBAnd = image2Orig.select('R')

# Determine the displacement by matching only the 'R' bAnds.
displacement = image2RedBAnd.displacement(**{
  'referenceImage': image1RedBAnd,
  'maxOffset': 50.0,
  'patchWidth': 100.0
})

# Compute image offset And direction.
offset = displacement.select('dx').hypot(displacement.select('dy'))
angle = displacement.select('dx').atan2(displacement.select('dy'))

# Display offset distance And angle.
Map.addLayer(offset, {'min':0, 'max': 20}, 'offset')
Map.addLayer(angle, {'min': -math.pi, 'max': math.pi}, 'angle')
Map.setCenter(37.44,0.58, 15)


# Use the computed displacement to register all Original bAnds.
registered = image2Orig.displace(displacement)

# Show the results of co-registering the images.
visParams = {'bands': ['R', 'G', 'B'], 'max': 4000}
Map.addLayer(image1Orig, visParams, 'Reference')
Map.addLayer(image2Orig, visParams, 'BefOre Registration')
Map.addLayer(registered, visParams, 'After Registration')


alsoRegistered = image2Orig.register(**{
  'referenceImage': image1Orig,
  'maxOffset': 50.0,
  'patchWidth': 100.0
})
Map.addLayer(alsoRegistered, visParams, 'Also Registered')

