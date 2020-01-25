import ee 
from ee_plugin import Map 

dataset = ee.Image('USGS/NED')
elevation = dataset.select('elevation')
elevationVis = {
  'min': 0.0,
  'max': 4000.0,
  'gamma': 1.6,
}
Map.setCenter(-100.55, 40.71, 5)
Map.addLayer(elevation, elevationVis, 'Elevation')
