import ee 
from ee_plugin import Map 

dataset = ee.ImageCollection('NRCan/CDEM')
elevation = dataset.select('elevation').mosaic()
elevationVis = {
  'min': -50.0,
  'max': 1500.0,
  'palette': ['0905ff', 'ffefc4', 'ffffff'],
}
Map.setCenter(-139.3643, 63.3213, 9)
Map.addLayer(elevation, elevationVis, 'Elevation')
