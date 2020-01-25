import ee 
from ee_plugin import Map 

# Load Landsat 5 data, filter by date and bounds.
collection = ee.ImageCollection('LANDSAT/LT05/C01/T2') \
  .filterDate('1987-01-01', '1990-05-01') \
  .filterBounds(ee.Geometry.Point(25.8544, -18.08874))

# Also filter the collection by the IMAGE_QUALITY property.
filtered = collection \
  .filterMetadata('IMAGE_QUALITY', 'equals', 9)

# Create two composites to check the effect of filtering by IMAGE_QUALITY.
badComposite = ee.Algorithms.Landsat.simpleComposite(collection, 75, 3)
goodComposite = ee.Algorithms.Landsat.simpleComposite(filtered, 75, 3)

# Display the composites.
Map.setCenter(25.8544, -18.08874, 13)
Map.addLayer(badComposite,
             {'bands': ['B3', 'B2', 'B1'], 'gain': 3.5},
             'bad composite')
Map.addLayer(goodComposite,
             {'bands': ['B3', 'B2', 'B1'], 'gain': 3.5},
             'good composite')

