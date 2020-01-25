import ee
from ee_plugin import Map

# Add some data to the Map
dem = ee.Image("JAXA/ALOS/AW3D30_V1_1").select('MED')
Map.addLayer(dem, {'min': 0, 'max': 5000, 'palette': ['000000', 'ffffff'] }, 'DEM', True)

# TEST Map.setCenter
Map.setCenter(0, 28, 2.5)
