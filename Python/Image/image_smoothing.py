# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Image/image_smoothing.py


import ee
from ee_plugin import Map

image = ee.Image('srtm90_v4')

smoothed = image.reduceNeighborhood(**{
    'reducer': ee.Reducer.mean(),
    'kernel': ee.Kernel.square(3),
})

# vis_params = {'min': 0, 'max': 3000}
# Map.addLayer(image, vis_params, 'SRTM original')
# Map.addLayer(smooth, vis_params, 'SRTM smoothed')
Map.setCenter(-112.40, 42.53, 12)
Map.addLayer(ee.Terrain.hillshade(image), {}, 'Original hillshade')
Map.addLayer(ee.Terrain.hillshade(smoothed), {}, 'Smoothed hillshade')
