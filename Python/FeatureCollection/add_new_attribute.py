import ee 
from ee_plugin import Map 

# This function creates a new property that is the sum of two existing properties.
def addField(feature):
  sum = ee.Number(feature.get('property1')).add(feature.get('property2'))
  return feature.set({'sum': sum})

# Create a FeatureCollection from a list of Features.
features = ee.FeatureCollection([
  ee.Feature(ee.Geometry.Point(-122.4536, 37.7403),
    {'property1': 100, 'property2': 100}),
    ee.Feature(ee.Geometry.Point(-118.2294, 34.039),
    {'property1': 200, 'property2': 300}),
])

# Map the function over the collection.
featureCollection = features.map(addField)

# Print the entire FeatureCollection.
print(featureCollection.getInfo())

# Print a selected property of one Feature.
print(featureCollection.first().get('sum').getInfo())


