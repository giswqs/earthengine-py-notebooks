import ee
from ee_plugin import Map
image = ee.Image('srtm90_v4')
# path = image.getDownloadUrl({
#     'scale': 30,
#     'crs': 'EPSG:4326',
#     'region': '[[-120, 35], [-119, 35], [-119, 34], [-120, 34]]'
# })
vis_params = {'min': 0, 'max': 3000}
Map.addLayer(image, vis_params, 'SRTM')