import ee 
from ee_plugin import Map 

def areaDiff(feature):
  area = feature.geometry().area().divide(1000 * 1000)
  # Compute the differece between computed area and the area property.
  diff = area.subtract(ee.Number.parse(feature.get('areasqkm')))
  # Return the feature with the squared difference set to the 'diff' property.
  return feature.set('diff', diff.pow(2))


# Load watersheds from a data table and filter to the continental US.
sheds = ee.FeatureCollection('USGS/WBD/2017/HUC06') \
  .filterBounds(ee.Geometry.Rectangle(-127.18, 19.39, -62.75, 51.29))

# This function computes the squared difference between an area property
# and area computed directly from the feature's geometry.
# areaDiff = function(feature) {
#   # Compute area in sq. km directly from the geometry.
#   area = feature.geometry().area().divide(1000 * 1000)
#   # Compute the differece between computed area and the area property.
#   diff = area.subtract(ee.Number.parse(feature.get('areasqkm')))
#   # Return the feature with the squared difference set to the 'diff' property.
#   return feature.set('diff', diff.pow(2))
# }

# Calculate RMSE for population of difference pairs.
rmse = ee.Number(
  # Map the difference function over the collection.
  sheds.map(areaDiff)
  # Reduce to get the mean squared difference. \
  .reduceColumns(ee.Reducer.mean(), ['diff']) \
  .get('mean')
) \
.sqrt()

# Print the result.
print('RMSE=', rmse.getInfo())

