import ee 
from ee_plugin import Map 

# Make an area of interest geometry centered on San Francisco.
point = ee.Geometry.Point(-122.1899, 37.5010)
aoi = point.buffer(10000)

# Import a Landsat 8 image, subset the thermal band, and clip to the
# area of interest.
kelvin = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318') \
  .select(['B10'], ['kelvin']) \
  .clip(aoi)

# Display the thermal band.
# Map.centerObject(point, 13)
Map.setCenter(-122.1899, 37.5010, 13)
Map.addLayer(kelvin, {'min': 288, 'max': 305}, 'Kelvin')


# Threshold the thermal band to set hot pixels as value 1 and not as 0.
hotspots = kelvin.gt(303) \
  .selfMask() \
  .rename('hotspots')

# Display the thermal hotspots on the Map.
Map.addLayer(hotspots, {'palette': 'FF0000'}, 'Hotspots')


# Uniquely label the hotspot image objects.
objectId = hotspots.connectedComponents(**{
  'connectedness': ee.Kernel.plus(1),
  'maxSize': 128
})

# Display the uniquely ID'ed objects to the Map.
Map.addLayer(objectId.randomVisualizer(), {}, 'Objects')


# Compute the number of pixels in each object defined by the "labels" band.
objectSize = objectId.select('labels') \
  .connectedPixelCount(**{
    'maxSize': 128, 'eightConnected': False
  })

# Display object pixel count to the Map.
Map.addLayer(objectSize, {}, 'Object n pixels')


# Get a pixel area image.
pixelArea = ee.Image.pixelArea()

# Multiply pixel area by the number of pixels in an object to calculate
# the object area. The result is an image where each pixel
# of an object relates the area of the object in m^2.
objectArea = objectSize.multiply(pixelArea)

# Display object area to the Map.
Map.addLayer(objectArea, {}, 'Object area m^2')


# Threshold the `objectArea` image to define a mask that will mask out
# objects below a given size (1 hectare in this case).
areaMask = objectArea.gte(10000)

# Update the mask of the `objectId` layer defined previously using the
# minimum area mask just defined.
objectId = objectId.updateMask(areaMask)
Map.addLayer(objectId, {}, 'Large hotspots')


# Make a suitable image for `reduceConnectedComponents()` by adding a label
# band to the `kelvin` temperature image.
kelvin = kelvin.addBands(objectId.select('labels'))

# Calculate the mean temperature per object defined by the previously added
# "labels" band.
patchTemp = kelvin.reduceConnectedComponents(**{
  'reducer': ee.Reducer.mean(),
  'labelBand': 'labels'
})

# Display object mean temperature to the Map.
Map.addLayer(
  patchTemp,
  {'min': 303, 'max': 304, 'palette': ['yellow', 'red']},
  'Mean temperature'
)
