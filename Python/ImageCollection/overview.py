import ee 
from ee_plugin import Map 

# Create arbitrary constant images.
constant1 = ee.Image(1)
constant2 = ee.Image(2)

# Create a collection by giving a list to the constructor.
collectionFromConstructor = ee.ImageCollection([constant1, constant2])
print('collectionFromConstructor: ', collectionFromConstructor.getInfo())

# Create a collection with fromImages().
collectionFromImages = ee.ImageCollection.fromImages(
  [ee.Image(3), ee.Image(4)])
print('collectionFromImages: ', collectionFromImages.getInfo())

# Merge two collections.
mergedCollection = collectionFromConstructor.merge(collectionFromImages)
print('mergedCollection: ', mergedCollection.getInfo())

# # Create a toy FeatureCollection
# features = ee.FeatureCollection(
#   [ee.Feature({}, {'foo': 1}), ee.Feature({}, {'foo': 2})])

# # Create an ImageCollection from the FeatureCollection
# # by mapping a function over the FeatureCollection.
# images = features.map(function(feature) {
#   return ee.Image(ee.Number(feature.get('foo')))
# })

# # Print the resultant collection.
# print('Image collection: ', images)

