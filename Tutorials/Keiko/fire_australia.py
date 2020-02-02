'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Tutorials/Keiko/fire_australia.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Tutorials/Keiko/fire_australia.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Tutorials/Keiko/fire_australia.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Tutorials/Keiko/fire_australia.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
</table>
'''

# %%
'''
## Install Earth Engine API
Install the [Earth Engine Python API](https://developers.google.com/earth-engine/python_install) and [geehydro](https://github.com/giswqs/geehydro). The **geehydro** Python package builds on the [folium](https://github.com/python-visualization/folium) package and implements several methods for displaying Earth Engine data layers, such as `Map.addLayer()`, `Map.setCenter()`, `Map.centerObject()`, and `Map.setOptions()`.
The magic command `%%capture` can be used to hide output from a specific cell. Uncomment these lines if you are running this notebook for the first time.
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
if you are running this notebook for the first time or if you are getting an authentication error.  
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
# Credits to: Keiko Nomura, Senior Analyst, Space Intelligence Ltd
# Source: https://medium.com/google-earth/10-tips-for-becoming-an-earth-engine-expert-b11aad9e598b
# GEE JS: https://code.earthengine.google.com/?scriptPath=users%2Fnkeikon%2Fmedium%3Afire_australia 

geometry = ee.Geometry.Polygon(
        [[[153.02512376008724, -28.052192238512877],
          [153.02512376008724, -28.702237664294238],
          [153.65683762727474, -28.702237664294238],
          [153.65683762727474, -28.052192238512877]]])
Map.centerObject(ee.FeatureCollection(geometry), 10)

# Use clear images from May and Dec 2019
imageMay = ee.Image('COPERNICUS/S2_SR/20190506T235259_20190506T235253_T56JNP')
imageDec = ee.Image('COPERNICUS/S2_SR/20191202T235239_20191202T235239_T56JNP')

Map.addLayer(imageMay, {
  'bands': ['B4', 'B3', 'B2'],
  'min': 0,
  'max': 1800
}, 'May 2019 (True colours)')
Map.addLayer(imageDec, {
  'bands': ['B4', 'B3', 'B2'],
  'min': 0,
  'max': 1800
}, 'Dec 2019 (True colours)')

# Compute NDVI and use grey colour for areas with NDVI < 0.8 in May 2019
NDVI = imageMay.normalizedDifference(['B8', 'B4']).rename('NDVI')
grey = imageMay.mask(NDVI.select('NDVI').lt(0.8))

Map.addLayer(grey, {
  'bands': ['B3', 'B3', 'B3'],
  'min': 0,
  'max': 1800,
  'gamma': 1.5
}, 'grey (base)')

# Export as mosaic. Alternatively you can also use blend().
mosaicDec = ee.ImageCollection([
  imageDec.visualize(**{
    'bands': ['B4', 'B3', 'B2'],
    'min': 0,
    'max': 1800
  }),
  grey.visualize(**{
    'bands': ['B3', 'B3', 'B3'],
    'min': 0,
    'max': 1800
  }),
]).mosaic()

mosaicMay = ee.ImageCollection([
  imageMay.visualize(**{
    'bands': ['B4', 'B3', 'B2'],
    'min': 0,
    'max': 1800
  }),
  grey.visualize(**{
    'bands': ['B3', 'B3', 'B3'],
    'min': 0,
    'max': 1800
  }),
]).mosaic()

# Export.image.toDrive({
#   'image': mosaicMay,
#   description: 'May',
#   'region': geometry,
#   crs: 'EPSG:3857',
#   'scale': 10
# })

# Export.image.toDrive({
#   'image': mosaicDec,
#   description: 'Dec',
#   'region': geometry,
#   crs: 'EPSG:3857',
#   'scale': 10
# })

# ============ #
#  Topography  #
# ============ #

# Add topography by computing a hillshade using the terrain algorithms
elev = ee.Image('USGS/SRTMGL1_003')
shadeAll = ee.Terrain.hillshade(elev)
shade = shadeAll.mask(elev.gt(0)) # mask the sea

mayTR = ee.ImageCollection([
  imageMay.visualize(**{
    'bands': ['B4', 'B3', 'B2'],
    'min': 0,
    'max': 1800
  }),
  shade.visualize(**{
    'bands': ['hillshade', 'hillshade', 'hillshade'],
    'opacity': 0.2
  }),
]).mosaic()

highVeg = NDVI.gte(0.8).visualize(**{
  'min': 0,
  'max': 1
})

Map.addLayer(mayTR.mask(highVeg), {
  'gamma': 0.8
}, 'May (with topography)',False)

# Convert the visualized elevation to HSV, first converting to [0, 1] data.
hsv = mayTR.divide(255).rgbToHsv()
# Select only the hue and saturation bands.
hs = hsv.select(0, 1)
# Convert the hillshade to [0, 1] data, as expected by the HSV algorithm.
v = shade.divide(255)
# Create a visualization image by converting back to RGB from HSV.
# Note the cast to byte in order to export the image correctly.
rgb = hs.addBands(v).hsvToRgb().multiply(255).byte()

Map.addLayer(rgb.mask(highVeg), {
  'gamma': 0.5
}, 'May (topography visualised)')

# Export the image
mayTRMosaic = ee.ImageCollection([
  rgb.mask(highVeg).visualize(**{
  'gamma': 0.5}),
  grey.visualize(**{
    'bands': ['B3', 'B3', 'B3'],
    'min': 0,
    'max': 1800
  }),
]).mosaic()

# Export.image.toDrive({
#   'image': mayTRMosaic,
#   description: 'MayTerrain',
#   'region': geometry,
#   crs: 'EPSG:3857',
#   'scale': 10
# })

decTR = ee.ImageCollection([
  imageDec.visualize(**{
    'bands': ['B4', 'B3', 'B2'],
    'min': 0,
    'max': 1800
  }),
  shade.visualize(**{
    'bands': ['hillshade', 'hillshade', 'hillshade'],
    'opacity': 0.2
  }),
]).mosaic()

Map.addLayer(decTR.mask(highVeg), {
  'gamma': 0.8
}, 'Dec (with topography)',False)

# Convert the visualized elevation to HSV, first converting to [0, 1] data.
hsv = decTR.divide(255).rgbToHsv()
# Select only the hue and saturation bands.
hs = hsv.select(0, 1)
# Convert the hillshade to [0, 1] data, as expected by the HSV algorithm.
v = shade.divide(255)
# Create a visualization image by converting back to RGB from HSV.
# Note the cast to byte in order to export the image correctly.
rgb = hs.addBands(v).hsvToRgb().multiply(255).byte()

Map.addLayer(rgb.mask(highVeg), {
  'gamma': 0.5
}, 'Dec (topography visualised)')

# Export the image
decTRMosaic = ee.ImageCollection([
  rgb.mask(highVeg).visualize(**{
    'gamma': 0.5
  }),
  grey.visualize(**{
    'bands': ['B3', 'B3', 'B3'],
    'min': 0,
    'max': 1800
  }),
]).mosaic()

# Export.image.toDrive({
#   'image': decTRMosaic,
#   description: 'DecTerrain',
#   'region': geometry,
#   crs: 'EPSG:3857',
#   'scale': 10
# })


# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map