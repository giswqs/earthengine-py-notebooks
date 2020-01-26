'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Algorithms/Segmentation/segmentation_snic.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Algorithms/Segmentation/segmentation_snic.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Algorithms/Segmentation/segmentation_snic.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Algorithms/Segmentation/segmentation_snic.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
</table>
'''

# %%
'''
## Install Earth Engine API
Install the [Earth Engine Python API](https://developers.google.com/earth-engine/python_install) and [geehydro](https://github.com/giswqs/geehydro). The **geehydro** Python package builds on the [folium](https://github.com/python-visualization/folium) package and implements several methods for displaying Earth Engine data layers, such as `Map.addLayer()`, `Map.setCenter()`, `Map.centerObject()`, and `Map.setOptions()`.
The magic command `%%capture` can be used to hide output from a specific cell.
'''


# %%
# %%capture
# !pip install earthengine-api
# !pip install geehydro

# %%
'''
Import libraries
'''


# %%
import ee
import folium
import geehydro

# %%
'''
Authenticate and initialize Earth Engine API. You only need to authenticate the Earth Engine API once. Uncomment the line `ee.Authenticate()` 
if you are running this notebook for this first time or if you are getting an authentication error.  
'''


# %%
# ee.Authenticate()
ee.Initialize()

# %%
'''
## Create an interactive map 
This step creates an interactive map using [folium](https://github.com/python-visualization/folium). The default basemap is the OpenStreetMap. Additional basemaps can be added using the `Map.setOptions()` function. 
The optional basemaps can be `ROADMAP`, `SATELLITE`, `HYBRID`, `TERRAIN`, or `ESRI`.
'''

# %%
Map = folium.Map(location=[40, -100], zoom_start=4)
Map.setOptions('HYBRID')

# %%
'''
## Add Earth Engine Python script 

'''

# %%
# imageCollection = ee.ImageCollection("USDA/NAIP/DOQQ"),
# geometry = ee.Geometry.Polygon(
#     [[[-121.89511299133301, 38.98496606984683],
#         [-121.89511299133301, 38.909335196675435],
#         [-121.69358253479004, 38.909335196675435],
#         [-121.69358253479004, 38.98496606984683]]], {}, False),
# geometry2 = ee.Geometry.Polygon(
#     [[[-108.34304809570307, 36.66975278349341],
#         [-108.34225416183466, 36.66977859999848],
#         [-108.34226489067072, 36.67042400981031],
#         [-108.34308028221125, 36.670380982657925]]]),
# imageCollection2 = ee.ImageCollection("USDA/NASS/CDL"),
# cdl2016 = ee.Image("USDA/NASS/CDL/2016")


# Map.centerObject(geometry, {}, 'roi')
# # Map.addLayer(ee.Image(1), {'palette': "white"})
# cdl2016 = cdl2016.select(0).clip(geometry)

# function erode(img, distance) {
#   d = (img.Not().unmask(1) \
#        .fastDistanceTransform(30).sqrt() \
#        .multiply(ee.Image.pixelArea().sqrt()))
#   return img.updateMask(d.gt(distance))
# }

# function dilate(img, distance) {
#   d = (img.fastDistanceTransform(30).sqrt() \
#        .multiply(ee.Image.pixelArea().sqrt()))
#   return d.lt(distance)
# }

# function expandSeeds(seeds) {
#   seeds = seeds.unmask(0).focal_max()
#   return seeds.updateMask(seeds)
# }

# bands = ["R", "G", "B", "N"]
# img = imageCollection \
#     .filterDate('2015-01-01', '2017-01-01') \
#     .filterBounds(geometry) \
#     .mosaic()
# img = ee.Image(img).clip(geometry).divide(255).select(bands)
# Map.addLayer(img, {'gamma': 0.8}, "RGBN", False)

# seeds = ee.Algorithms.Image.Segmentation.seedGrid(36)

# # Apply a softening.
# kernel = ee.Kernel.gaussian(3)
# img = img.convolve(kernel)
# Map.addLayer(img, {'gamma': 0.8}, "RGBN blur", False)

# # Compute and display NDVI, NDVI slices and NDVI gradient.
# ndvi = img.normalizedDifference(["N", "R"])
# # print(ui.Chart.image.histogram(ndvi, geometry, 10))
# Map.addLayer(ndvi, {'min':0, 'max':1, 'palette': ["black", "tan", "green", "darkgreen"]}, "NDVI", False)
# Map.addLayer(ndvi.gt([0, 0.2, 0.40, 0.60, 0.80, 1.00]).reduce('sum'), {'min':0, 'max': 6}, "NDVI steps", False)
# ndviGradient = ndvi.gradient().pow(2).reduce('sum').sqrt()
# Map.addLayer(ndviGradient, {'min':0, 'max':0.01}, "NDVI gradient", False)

# gradient = img.spectralErosion().spectralGradient('emd')
# Map.addLayer(gradient, {'min':0, 'max': 0.3}, "emd", False)

# # Run SNIC on the regular square grid.
# snic = ee.Algorithms.Image.Segmentation.SNIC({
#   'image': img,
#   'size': 32,
#   compactness: 5,
#   connectivity: 8,
#   neighborhoodSize:256,
#   seeds: seeds
# }).select(["R_mean", "G_mean", "B_mean", "N_mean", "clusters"], ["R", "G", "B", "N", "clusters"])

# clusters = snic.select("clusters")
# Map.addLayer(clusters.randomVisualizer(), {}, "clusters")
# Map.addLayer(snic, {'bands': ["R", "G", "B"], 'min':0, 'max':1, 'gamma': 0.8}, "means", False)
# Map.addLayer(expandSeeds(seeds))

# # Compute per-cluster stdDev.
# stdDev = img.addBands(clusters).reduceConnectedComponents(ee.Reducer.stdDev(), "clusters", 256)
# Map.addLayer(stdDev, {'min':0, 'max':0.1}, "StdDev")

# # Display outliers as transparent
# outliers = stdDev.reduce('sum').gt(0.25)
# Map.addLayer(outliers.updateMask(outliers.Not()), {}, "Outliers", False)

# # Within each outlier, find most distant member.
# distance = img.select(bands).spectralDistance(snic.select(bands), "sam").updateMask(outliers)
# maxDistance = distance.addBands(clusters).reduceConnectedComponents(ee.Reducer.max(), "clusters", 256)
# Map.addLayer(distance, {'min':0, 'max':0.3}, "max distance")
# Map.addLayer(expandSeeds(expandSeeds(distance.eq(maxDistance))), {'palette': ["red"]}, "second seeds")

# newSeeds = seeds.unmask(0).add(distance.eq(maxDistance).unmask(0))
# newSeeds = newSeeds.updateMask(newSeeds)

# # Run SNIC again with both sets of seeds.
# snic2 = ee.Algorithms.Image.Segmentation.SNIC({
#   'image': img,
#   'size': 32,
#   compactness: 5,
#   connectivity: 8,
#   neighborhoodSize: 256,
#   seeds: newSeeds
# }).select(["R_mean", "G_mean", "B_mean", "N_mean", "clusters"], ["R", "G", "B", "N", "clusters"])
# clusters2 = snic2.select("clusters")
# Map.addLayer(clusters2.randomVisualizer(), {}, "clusters 2")
# Map.addLayer(snic2, {'bands': ["R", "G", "B"], 'min':0, 'max':1, 'gamma': 0.8}, "means", False)

# # Compute outliers again.
# stdDev2 = img.addBands(clusters2).reduceConnectedComponents(ee.Reducer.stdDev(), "clusters", 256)
# Map.addLayer(stdDev2, {'min':0, 'max':0.1}, "StdDev 2")
# outliers2 = stdDev2.reduce('sum').gt(0.25)
# outliers2 = outliers2.updateMask(outliers2.Not())
# Map.addLayer(outliers2, {}, "Outliers 2", False)

# # Show the final set of seeds.
# Map.addLayer(expandSeeds(newSeeds), {'palette': "white"}, "newSeeds")
# Map.addLayer(expandSeeds(distance.eq(maxDistance)), {'palette': ["red"]}, "second seeds")

# # Area, Perimeter, Width and Height (using snic1 for speed)
# area = ee.Image.pixelArea().addBands(clusters).reduceConnectedComponents(ee.Reducer.sum(), "clusters", 256)
# Map.addLayer(area, {'min':50000, 'max': 500000}, "Cluster Area")
# minMax = clusters.reduceNeighborhood(ee.Reducer.minMax(), ee.Kernel.square(1))

# perimeterPixels = minMax.select(0).neq(minMax.select(1)).rename('perimeter')
# Map.addLayer(perimeterPixels, {'min': 0, 'max': 1}, 'perimeterPixels')

# perimeter = perimeterPixels.addBands(clusters) \
#     .reduceConnectedComponents(ee.Reducer.sum(), 'clusters', 256)
# Map.addLayer(perimeter, {'min': 100, 'max': 400}, 'Perimeter size', False)

# sizes = ee.Image.pixelLonLat().addBands(clusters).reduceConnectedComponents(ee.Reducer.minMax(), "clusters", 256)
# width = sizes.select("longitude_max").subtract(sizes.select("longitude_min"))
# height = sizes.select("latitude_max").subtract(sizes.select("latitude_min"))
# Map.addLayer(width, {'min':0, 'max':0.02}, "Cluster width")
# Map.addLayer(height, {'min':0, 'max':0.02}, "Cluster height")


# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map