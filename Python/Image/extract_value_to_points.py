import ee
from ee_plugin import Map

# Input imagery is a cloud-free Landsat 8 composite.
l8 = ee.ImageCollection('LANDSAT/LC08/C01/T1')

image = ee.Algorithms.Landsat.simpleComposite(**{
    'collection': l8.filterDate('2018-01-01', '2018-12-31'),
    'asFloat': True
})

# Use these bands for prediction.
bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'B11']

# Load training points. The numeric property 'class' stores known labels.
points = ee.FeatureCollection('GOOGLE/EE/DEMOS/demo_landcover_labels')

# This property of the table stores the land cover labels.
label = 'landcover'

# Overlay the points on the imagery to get training.
training = image.select(bands).sampleRegions(**{
    'collection': points,
    'properties': [label],
    'scale': 30
})

# Define visualization parameters in an object literal.
vizParams = {'bands': ['B5', 'B4', 'B3'],
             'min': 0, 'max': 1, 'gamma': 1.3}


Map.centerObject(points, 10)
Map.addLayer(image, vizParams, 'Image')
Map.addLayer(points, {'color': "yellow"}, 'Training points')

first = training.first()
print(first.getInfo())
