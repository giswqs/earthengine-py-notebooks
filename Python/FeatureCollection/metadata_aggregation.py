import ee 
from ee_plugin import Map 

def cal_area(feature):
    num = ee.Number.parse(feature.get('areasqkm'))
    return feature.set('areasqkm', num)

# Load watersheds from a data table.
sheds = ee.FeatureCollection('USGS/WBD/2017/HUC06') \
  .filterBounds(ee.Geometry.Rectangle(-127.18, 19.39, -62.75, 51.29)) \
  .map(cal_area)

# Display the table and print its first element.
# Map.addLayer(sheds, {}, 'watersheds')
Map.addLayer(ee.Image().paint(sheds, 1, 2), {}, 'watersheds')
print('First watershed', sheds.first().getInfo())

# Print the number of watersheds.
print('Count:', sheds.size().getInfo())

# Print stats for an area property.
# print('Area stats:', sheds.aggregate_stats('areasqkm').getInfo())
