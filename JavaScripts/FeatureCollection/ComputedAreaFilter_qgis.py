import ee 
from ee_plugin import Map 

# Computed area filter.
# Find US counties smaller than 3k square kilometers in area.

# Load counties from TIGER boundaries table
counties = ee.FeatureCollection('TIGER/2016/Counties')

# Map a function over the counties to set the area of each.

def func_blc(f):
  # Compute area in square meters.  Convert to hectares.
  areaHa = f.area().divide(100 * 100)

  # A new property called 'area' will be set on each feature.
  return f.set({'area': areaHa})

countiesWithArea = counties.map(func_blc)








# Filter to get only smaller counties.
smallCounties = countiesWithArea.filter(ee.Filter.lt('area', 3e5))

Map.addLayer(smallCounties, {'color': '900000'})

Map.setCenter(-119.7, 38.26, 7)
