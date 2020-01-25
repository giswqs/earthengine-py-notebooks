import ee 
from ee_plugin import Map 

# Make a feature and set some properties.
feature = ee.Feature(ee.Geometry.Point([-122.22599, 37.17605])) \
  .set('genus', 'Sequoia').set('species', 'sempervirens')

# Get a property from the feature.
species = feature.get('species')
print(species.getInfo())

# Set a new property.
feature = feature.set('presence', 1)

# Overwrite the old properties with a new dictionary.
newDict = {'genus': 'Brachyramphus', 'species': 'marmoratus'}
feature = feature.set(newDict)

# Check the result.
print(feature.getInfo())

