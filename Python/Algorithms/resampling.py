import ee 
from ee_plugin import Map 

# Load a Landsat image over San Francisco, California, UAS.
landsat = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20160323')

# Set display and visualization parameters.
Map.setCenter(-122.37383, 37.6193, 15)
visParams = {'bands': ['B4', 'B3', 'B2'], 'max': 0.3}

# Display the Landsat image using the default nearest neighbor resampling.
# when reprojecting to Mercator for the Code Editor map.
Map.addLayer(landsat, visParams, 'original image')

# Force the next reprojection on this image to use bicubic resampling.
resampled = landsat.resample('bicubic')

# Display the Landsat image using bicubic resampling.
Map.addLayer(resampled, visParams, 'resampled')
