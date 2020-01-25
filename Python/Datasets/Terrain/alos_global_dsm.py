import ee 
from ee_plugin import Map 

dataset = ee.Image('JAXA/ALOS/AW3D30_V1_1')
elevation = dataset.select('AVE')
elevationVis = {
  'min': 0.0,
  'max': 4000.0,
  'palette': ['0000ff', '00ffff', 'ffff00', 'ff0000', 'ffffff'],
}
Map.setCenter(136.85, 37.37, 4)
Map.addLayer(elevation, elevationVis, 'Elevation')
