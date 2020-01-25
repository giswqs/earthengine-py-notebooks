import ee 
from ee_plugin import Map 

# Load a raw Landsat scene and display it.
raw = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318')
Map.centerObject(raw, 10)
Map.addLayer(raw, {'bands': ['B4', 'B3', 'B2'], 'min': 6000, 'max': 12000}, 'raw')

# Convert the raw data to radiance.
radiance = ee.Algorithms.Landsat.calibratedRadiance(raw)
Map.addLayer(radiance, {'bands': ['B4', 'B3', 'B2'], 'max': 90}, 'radiance')

# Convert the raw data to top-of-atmosphere reflectance.
toa = ee.Algorithms.Landsat.TOA(raw)

Map.addLayer(toa, {'bands': ['B4', 'B3', 'B2'], 'max': 0.2}, 'toa reflectance')

