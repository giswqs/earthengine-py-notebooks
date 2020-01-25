import ee
from ee_plugin import Map
img = ee.Image("COPERNICUS/S2_SR/20191115T074201_20191115T075706_T37MBM") 
ndvi = img.normalizedDifference(['B8','B4'])
pal = ["red","yellow","green"]
Map.setCenter(36.9,-7.7, 12)
Map.addLayer(ndvi,{'min':0,'max':0.8,'palette':pal},'NDVI')