import ee
from ee_plugin import Map

# add some data to the Map
dem = ee.Image("AHN/AHN2_05M_RUW")
Map.addLayer(dem, {'min': -5, 'max': 50, 'palette': ['000000', 'ffffff'] }, 'DEM', True)

# zoom in somewhere
Map.setCenter(4.4585, 52.0774, 15)

# TEST
Map.setZoom(10)
