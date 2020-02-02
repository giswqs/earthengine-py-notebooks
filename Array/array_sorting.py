'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Array/array_sorting.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Array/array_sorting.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Array/array_sorting.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Array/array_sorting.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Define an arbitrary region of interest as a point.
roi = ee.Geometry.Point(-122.26032, 37.87187)

# Use these bands.
bandNames = ee.List(['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'B11'])

# Load a Landsat 8 collection.
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
  .select(bandNames) \
  .filterBounds(roi) \
  .filterDate('2014-06-01', '2014-12-31') \
  .map(lambda image: ee.Algorithms.Landsat.simpleCloudScore(image))

# Convert the collection to an array.
array = collection.toArray()

# Label of the axes.
imageAxis = 0
bandAxis = 1

# Get the cloud slice and the bands of interest.
bands = array.arraySlice(bandAxis, 0, bandNames.length())
clouds = array.arraySlice(bandAxis, bandNames.length())

# Sort by cloudiness.
sorted = bands.arraySort(clouds)

# Get the least cloudy images, 20% of the total.
numImages = sorted.arrayLength(imageAxis).multiply(0.2).int()
leastCloudy = sorted.arraySlice(imageAxis, 0, numImages)

# Get the mean of the least cloudy images by reducing along the image axis.
mean = leastCloudy.arrayReduce(**{
  'reducer': ee.Reducer.mean(),
  'axes': [imageAxis]
})

# Turn the reduced array image into a multi-band image for display.
meanImage = mean.arrayProject([bandAxis]).arrayFlatten([bandNames])
Map.centerObject(ee.FeatureCollection(roi), 12)
Map.addLayer(meanImage, {'bands': ['B5', 'B4', 'B2'], 'min': 0, 'max': 0.5}, 'Mean Image')



# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map