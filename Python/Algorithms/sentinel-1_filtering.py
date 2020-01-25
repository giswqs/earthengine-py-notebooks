import ee 
from ee_plugin import Map 

# Load the Sentinel-1 ImageCollection.
sentinel1 = ee.ImageCollection('COPERNICUS/S1_GRD') \
    .filterBounds(ee.Geometry.Point(-122.37383, 37.6193))

# Filter by metadata properties.
vh = sentinel1 \
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH')) \
  .filter(ee.Filter.eq('instrumentMode', 'IW'))

# Filter to get images from different look angles.
vhAscending = vh.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))
vhDescending = vh.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))

# Create a composite from means at different polarizations and look angles.
composite = ee.Image.cat([
  vhAscending.select('VH').mean(),
  ee.ImageCollection(vhAscending.select('VV').merge(vhDescending.select('VV'))).mean(),
  vhDescending.select('VH').mean()
]).focal_median()

# Display as a composite of polarization and backscattering characteristics.
Map.setCenter(-122.37383, 37.6193, 10)
Map.addLayer(composite, {'min': [-25, -20, -25], 'max': [0, 10, 0]}, 'composite')

