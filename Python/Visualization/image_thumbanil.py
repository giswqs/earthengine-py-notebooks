import ee
from ee_plugin import Map

# Fetch a digital elevation model.
image = ee.Image('CGIAR/SRTM90_V4')

# Request a default thumbnail of the DEM with defined linear stretch.
# Set masked pixels (ocean) to 1000 so they map as gray.
thumbnail1 = image.unmask(1000).getThumbURL({
  'min': 0,
  'max': 3000
})
print('Thumbnail:', thumbnail1)

# # Specify region by GeoJSON, define palette, set size of the larger aspect dimension.
# thumbnail2 = image.getThumbURL({
#   'min': 0,
#   'max': 3000,
#   'palette': ['00A600','63C600','E6E600','E9BD3A','ECB176','EFC2B3','F2F2F2'],
#   'dimensions': 500,
#   'region': ee.Geometry.Rectangle([-84.6, -55.9, -32.9, 15.7]),
# })
# print('GeoJSON region, palette, and max dimension:', thumbnail2)

# # Specify region by list of points and set display CRS as Web Mercator.
# thumbnail3 = image.getThumbURL({
#   'min': 0,
#   'max': 3000,
#   'palette': ['00A600','63C600','E6E600','E9BD3A','ECB176','EFC2B3','F2F2F2'],
#   'region': [[-84.6, 15.7], [-84.6, -55.9], [-32.9, -55.9]],
#   'crs': 'EPSG:3857'
# })
# print('Linear ring region and specified crs', thumbnail3)