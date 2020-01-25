import ee 
from ee_plugin import Map 

def addArea(feature):
    return feature.set({'areaHa': feature.geometry().area().divide(100 * 100)})

# Load watersheds from a data table.
sheds = ee.FeatureCollection('USGS/WBD/2017/HUC06')

# This function computes the feature's geometry area and adds it as a property.
# addArea = function(feature) {
#   return feature.set({areaHa: feature.geometry().area().divide(100 * 100)})
# }

# Map the area getting function over the FeatureCollection.
areaAdded = sheds.map(addArea)

# Print the first feature from the collection with the added property.
print('First feature:', areaAdded.first().getInfo())

