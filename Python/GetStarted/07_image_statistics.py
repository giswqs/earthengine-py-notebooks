import ee 
from ee_plugin import Map 

# Load and display a Landsat TOA image.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')
Map.addLayer(image, {'bands': ['B4', 'B3', 'B2'], 'max': 0.3}, 'Landsat 8')

# Create an arbitrary rectangle as a region and display it.
region = ee.Geometry.Rectangle(-122.2806, 37.1209, -122.0554, 37.2413)
Map.centerObject(ee.FeatureCollection(region), 13)
Map.addLayer(ee.Image().paint(region, 0, 2), {}, 'Region')

# Get a dictionary of means in the region.  Keys are bandnames.
mean = image.reduceRegion(**{
  'reducer': ee.Reducer.mean(),
  'geometry': region,
  'scale': 30
})

print(mean.getInfo())