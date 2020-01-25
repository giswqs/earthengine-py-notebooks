import ee 
from ee_plugin import Map 

dataset = ee.Image('CSP/ERGo/1_0/US/CHILI')
usChili = dataset.select('constant')
usChiliVis = {
  'min': 0.0,
  'max': 255.0,
}
Map.setCenter(-105.8636, 40.3439, 11)
Map.addLayer(usChili, usChiliVis, 'US CHILI')
