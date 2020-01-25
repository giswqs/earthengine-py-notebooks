import ee 
from ee_plugin import Map 

# Load a MODIS EVI image.
modis = ee.Image(ee.ImageCollection('MODIS/006/MOD13A1').first()) \
    .select('EVI')

# Display the EVI image near La Honda, California.
Map.setCenter(-122.3616, 37.5331, 12)
Map.addLayer(modis, {'min': 2000, 'max': 5000}, 'MODIS EVI')

# Get information about the MODIS projection.
modisProjection = modis.projection()
print('MODIS projection:', modisProjection.getInfo())

# Load and display forest cover data at 30 meters resolution.
forest = ee.Image('UMD/hansen/global_forest_change_2015') \
    .select('treecover2000')
Map.addLayer(forest, {'max': 80}, 'forest cover 30 m')

# Get the forest cover data at MODIS scale and projection.
forestMean = forest \
    .reduceResolution(**{
      'reducer': ee.Reducer.mean(),
      'maxPixels': 1024
    }) \
    .reproject(**{
      'crs': modisProjection
    })

# Display the aggregated, reprojected forest cover data.
Map.addLayer(forestMean, {'max': 80}, 'forest cover at MODIS scale')
