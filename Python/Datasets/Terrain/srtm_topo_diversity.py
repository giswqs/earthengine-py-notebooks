import ee 
from ee_plugin import Map 

dataset = ee.Image('CSP/ERGo/1_0/Global/SRTM_topoDiversity')
srtmTopographicDiversity = dataset.select('constant')
srtmTopographicDiversityVis = {
  'min': 0.0,
  'max': 1.0,
}
Map.setCenter(-111.313, 39.724, 6)
Map.addLayer(
    srtmTopographicDiversity, srtmTopographicDiversityVis,
    'SRTM Topographic Diversity')
