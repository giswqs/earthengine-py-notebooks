import ee 
from ee_plugin import Map 

# Load a raw Landsat 5 ImageCollection for a single year.
collection = ee.ImageCollection('LANDSAT/LT05/C01/T1') \
    .filterDate('2010-01-01', '2010-12-31')

# Create a cloud-free composite with default parameters.
composite = ee.Algorithms.Landsat.simpleComposite(collection)

# Create a cloud-free composite with custom parameters for
# cloud score threshold and percentile.
customComposite = ee.Algorithms.Landsat.simpleComposite(**{
  'collection': collection,
  'percentile': 75,
  'cloudScoreRange': 5
})

# Display the composites.
Map.setCenter(-122.3578, 37.7726, 10)
Map.addLayer(composite, {'bands': ['B4', 'B3', 'B2'], 'max': 128}, 'TOA composite')
Map.addLayer(customComposite, {'bands': ['B4', 'B3', 'B2'], 'max': 128},
    'Custom TOA composite')

