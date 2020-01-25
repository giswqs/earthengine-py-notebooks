import ee
from ee_plugin import Map

# get a single feature
countries = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
country = countries.filter(ee.Filter.eq('country_na', 'Ukraine'))
Map.addLayer(country, { 'color': 'orange' }, 'feature collection layer')

# TEST: center feature on a map
Map.centerObject(country)
