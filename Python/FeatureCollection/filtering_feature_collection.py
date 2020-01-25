import ee 
from ee_plugin import Map 

def cal_area(feature):
    num = ee.Number.parse(feature.get('areasqkm'))
    return feature.set('areasqkm', num)

# Load watersheds from a data table.
sheds = ee.FeatureCollection('USGS/WBD/2017/HUC06') \
  .map(cal_area)

# Define a region roughly covering the continental US.
continentalUS = ee.Geometry.Rectangle(-127.18, 19.39, -62.75, 51.29)

# Filter the table geographically: only watersheds in the continental US.
filtered = sheds.filterBounds(continentalUS)

# Check the number of watersheds after filtering for location.
print('Count after filter:', filtered.size().getInfo())

# Filter to get only larger continental US watersheds.
largeSheds = filtered.filter(ee.Filter.gt('areasqkm', 25000))

# Check the number of watersheds after filtering for size and location.
print('Count after filtering by size:', largeSheds.size().getInfo())

