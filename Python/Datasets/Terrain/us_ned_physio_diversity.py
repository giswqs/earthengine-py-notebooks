import ee 
from ee_plugin import Map 

dataset = ee.Image('CSP/ERGo/1_0/US/physioDiversity')
physiographicDiversity = dataset.select('b1')
physiographicDiversityVis = {
  'min': 0.0,
  'max': 1.0,
}
Map.setCenter(-94.625, 39.825, 7)
Map.addLayer(
    physiographicDiversity, physiographicDiversityVis,
    'Physiographic Diversity')
