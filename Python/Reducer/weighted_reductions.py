import ee 
from ee_plugin import Map 

# Load a Landsat 8 input image.
image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318')

# Creat an arbitrary region.
geometry = ee.Geometry.Rectangle(-122.496, 37.532, -121.554, 37.538)

# Make an NDWI image.  It will have one band named 'nd'.
ndwi = image.normalizedDifference(['B3', 'B5'])

# Compute the weighted mean of the NDWI image clipped to the region.
weighted = ndwi.clip(geometry) \
  .reduceRegion(**{
    'reducer': ee.Reducer.sum(),
    'geometry': geometry,
    'scale': 30}) \
  .get('nd')

# Compute the UN-weighted mean of the NDWI image clipped to the region.
unweighted = ndwi.clip(geometry) \
  .reduceRegion(**{
    'reducer': ee.Reducer.sum().unweighted(),
    'geometry': geometry,
    'scale': 30}) \
  .get('nd')

# Observe the difference between weighted and unweighted reductions.
print('weighted:', weighted.getInfo())
print('unweighted', unweighted.getInfo())

