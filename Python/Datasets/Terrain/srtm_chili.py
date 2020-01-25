import ee 
from ee_plugin import Map 

dataset = ee.Image('CSP/ERGo/1_0/Global/SRTM_CHILI')
srtmChili = dataset.select('constant')
srtmChiliVis = {
  'min': 0.0,
  'max': 255.0,
}
Map.setCenter(-105.8636, 40.3439, 11)
Map.addLayer(srtmChili, srtmChiliVis, 'SRTM CHILI')
