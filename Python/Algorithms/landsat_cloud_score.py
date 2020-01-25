import ee 
from ee_plugin import Map 

# Load a cloudy Landsat scene and display it.
cloudy_scene = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140926')
Map.centerObject(cloudy_scene)
Map.addLayer(cloudy_scene, {'bands': ['B4', 'B3', 'B2'], 'max': 0.4}, 'TOA', False)

# Add a cloud score band.  It is automatically called 'cloud'.
scored = ee.Algorithms.Landsat.simpleCloudScore(cloudy_scene)

# Create a mask from the cloud score and combine it with the image mask.
mask = scored.select(['cloud']).lte(20)

# Apply the mask to the image and display the result.
masked = cloudy_scene.updateMask(mask)
Map.addLayer(masked, {'bands': ['B4', 'B3', 'B2'], 'max': 0.4}, 'masked')

# Load a Landsat 8 composite and set the SENSOR_ID property.
mosaic = ee.Image(ee.ImageCollection('LANDSAT/LC8_L1T_8DAY_TOA').first()) \
  .set('SENSOR_ID', 'OLI_TIRS')

# Cloud score the mosaic and display the result.
scored_mosaic = ee.Algorithms.Landsat.simpleCloudScore(mosaic)
Map.addLayer(scored_mosaic, {'bands': ['B4', 'B3', 'B2'], 'max': 0.4},
    'TOA mosaic', False)



