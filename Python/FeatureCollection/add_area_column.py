# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/FeatureCollection/add_area_column.py

import ee 
from ee_plugin import Map 

fromFT = ee.FeatureCollection("users/wqs/Pipestem/Pipestem_HUC10")
# This function computes the feature's geometry area and adds it as a property.
def addArea(feature):
  return feature.set({'areaHa': feature.geometry().area().divide(100 * 100)})


# Map the area getting function over the FeatureCollection.
areaAdded = fromFT.map(addArea)
# Print the first feature from the collection with the added property.

first = areaAdded.first()
print('First feature: ', first.getInfo())
print("areaHa: ", first.get("areaHa").getInfo())
