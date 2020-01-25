# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/FeatureCollection/select_columns.py

import ee 
from ee_plugin import Map 

fc = ee.FeatureCollection('TIGER/2018/States')

print(fc.first().getInfo())

new_fc = fc.select(['STUSPS', 'NAME', 'ALAND'], ['abbr', 'name', 'area'])
print(new_fc.first().getInfo())

propertyNames = new_fc.first().propertyNames()
print(propertyNames.getInfo())