'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Array/array_transformations.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Array/array_transformations.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Array/array_transformations.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Array/array_transformations.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
import math
# This function masks the input with a threshold on the simple cloud score.
def cloudMask(img):
  cloudscore = ee.Algorithms.Landsat.simpleCloudScore(img).select('cloud')
  return img.updateMask(cloudscore.lt(50))

# cloudMask = function(img) {
#   cloudscore = ee.Algorithms.Landsat.simpleCloudScore(img).select('cloud')
#   return img.updateMask(cloudscore.lt(50))
# }

# This function computes the predictors and the response from the input.
def makeVariables(image):
  # Compute time of the image in fractional years relative to the Epoch.
  year = ee.Image(image.date().difference(ee.Date('1970-01-01'), 'year'))
  # Compute the season in radians, one cycle per year.
  season = year.multiply(2 * math.pi)
  # Return an image of the predictors followed by the response.
  return image.select() \
    .addBands(ee.Image(1)) \
    .addBands(year.rename('t')) \
    .addBands(season.sin().rename('sin')) \
    .addBands(season.cos().rename('cos')) \
    .addBands(image.normalizedDifference().rename('NDVI')) \
    .toFloat()

# Load a Landsat 5 image collection.
collection = ee.ImageCollection('LANDSAT/LT05/C01/T1_TOA') \
  .filterDate('2008-04-01', '2010-04-01')   \
  .filterBounds(ee.Geometry.Point(-122.2627, 37.8735)) \
  .map(cloudMask)  \
  .select(['B4', 'B3']) \
  .sort('system:time_start', True)

# # This function computes the predictors and the response from the input.
# makeVariables = function(image) {
#   # Compute time of the image in fractional years relative to the Epoch.
#   year = ee.Image(image.date().difference(ee.Date('1970-01-01'), 'year'))
#   # Compute the season in radians, one cycle per year.
#   season = year.multiply(2 * Math.PI)
#   # Return an image of the predictors followed by the response.
#   return image.select() \
#     .addBands(ee.Image(1))                                  # 0. constant \
#     .addBands(year.rename('t'))                             # 1. linear trend \
#     .addBands(season.sin().rename('sin'))                   # 2. seasonal \
#     .addBands(season.cos().rename('cos'))                   # 3. seasonal \
#     .addBands(image.normalizedDifference().rename('NDVI'))  # 4. response \
#     .toFloat()
# }

# Define the axes of variation in the collection array.
imageAxis = 0
bandAxis = 1

# Convert the collection to an array.
array = collection.map(makeVariables).toArray()

# Check the length of the image axis (number of images).
arrayLength = array.arrayLength(imageAxis)
# Update the mask to ensure that the number of images is greater than or
# equal to the number of predictors (the linear model is solveable).
array = array.updateMask(arrayLength.gt(4))

# Get slices of the array according to positions along the band axis.
predictors = array.arraySlice(bandAxis, 0, 4)
response = array.arraySlice(bandAxis, 4)

# Compute coefficients the easiest way.
coefficients3 = predictors.matrixSolve(response)

# Turn the results into a multi-band image.
coefficientsImage = coefficients3 \
  .arrayProject([0]) \
  .arrayFlatten([
    ['constant', 'trend', 'sin', 'cos']
])

print(coefficientsImage.getInfo())
Map.setCenter(-122.2627, 37.8735, 10)
Map.addLayer(coefficientsImage, {}, 'coefficientsImage')

# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map