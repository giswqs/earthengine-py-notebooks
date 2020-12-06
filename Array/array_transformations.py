# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Array/array_transformations.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Array/array_transformations.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Array/array_transformations.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
</table>
"""

# %%
"""
## Install Earth Engine API and geemap
Install the [Earth Engine Python API](https://developers.google.com/earth-engine/python_install) and [geemap](https://geemap.org). The **geemap** Python package is built upon the [ipyleaflet](https://github.com/jupyter-widgets/ipyleaflet) and [folium](https://github.com/python-visualization/folium) packages and implements several methods for interacting with Earth Engine data layers, such as `Map.addLayer()`, `Map.setCenter()`, and `Map.centerObject()`.
The following script checks if the geemap package has been installed. If not, it will install geemap, which automatically installs its [dependencies](https://github.com/giswqs/geemap#dependencies), including earthengine-api, folium, and ipyleaflet.
"""

# %%
# Installs geemap package
import subprocess

try:
    import geemap
except ImportError:
    print('Installing geemap ...')
    subprocess.check_call(["python", '-m', 'pip', 'install', 'geemap'])

# %%
import ee
import geemap

# %%
"""
## Create an interactive map 
The default basemap is `Google Maps`. [Additional basemaps](https://github.com/giswqs/geemap/blob/master/geemap/basemaps.py) can be added using the `Map.add_basemap()` function. 
"""

# %%
Map = geemap.Map(center=[40,-100], zoom=4)
Map

# %%
"""
## Add Earth Engine Python script 
"""

# %%
# Add Earth Engine dataset
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
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map