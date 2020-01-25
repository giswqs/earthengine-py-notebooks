import ee 
from ee_plugin import Map 

# Load a pre-computed Landsat composite for input.
input = ee.Image('LANDSAT/LE7_TOA_1YEAR/2001')

# Define a region in which to generate a sample of the input.
region = ee.Geometry.Rectangle(29.7, 30, 32.5, 31.7)

# Display the sample region.
Map.setCenter(31.5, 31.0, 8)
Map.addLayer(ee.Image().paint(region, 0, 2), {}, 'region')

# Make the training dataset.
training = input.sample(**{
  'region': region,
  'scale': 30,
  'numPixels': 5000
})

# Instantiate the clusterer and train it.
clusterer = ee.Clusterer.wekaKMeans(15).train(training)

# Cluster the input using the trained clusterer.
result = input.cluster(clusterer)

# Display the clusters with random colors.
Map.addLayer(result.randomVisualizer(), {}, 'clusters')
