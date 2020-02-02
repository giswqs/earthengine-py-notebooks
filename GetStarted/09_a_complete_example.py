'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/GetStarted/09_a_complete_example.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/GetStarted/09_a_complete_example.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=GetStarted/09_a_complete_example.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/GetStarted/09_a_complete_example.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# This function gets NDVI from a Landsat 8 image.


def addNDVI(image):
    return image.addBands(image.normalizedDifference(['B5', 'B4']))

# This function masks cloudy pixels.


def cloudMask(image):
    clouds = ee.Algorithms.Landsat.simpleCloudScore(image).select(['cloud'])
    return image.updateMask(clouds.lt(10))


# Load a Landsat collection, map the NDVI and cloud masking functions over it.
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
    .filterBounds(ee.Geometry.Point([-122.262, 37.8719])) \
    .filterDate('2014-03-01', '2014-05-31') \
    .map(addNDVI) \
    .map(cloudMask)

# Reduce the collection to the mean of each pixel and display.
meanImage = collection.reduce(ee.Reducer.mean())
vizParams = {'bands': ['B5_mean', 'B4_mean', 'B3_mean'], 'min': 0, 'max': 0.5}
Map.setCenter(-122.262, 37.8719, 10)
Map.addLayer(meanImage, vizParams, 'mean')

# Load a region in which to compute the mean and display it.
counties = ee.FeatureCollection('TIGER/2016/Counties')
santaClara = ee.Feature(counties.filter(
    ee.Filter.eq('NAME', 'Santa Clara')).first())
Map.addLayer(ee.Image().paint(santaClara, 0, 2), {
             'palette': 'yellow'}, 'Santa Clara')

# Get the mean of NDVI in the region.
mean = meanImage.select(['nd_mean']).reduceRegion(**{
    'reducer': ee.Reducer.mean(),
    'geometry': santaClara.geometry(),
    'scale': 30
})

# Print mean NDVI for the region.
print('Santa Clara spring mean NDVI:', mean.get('nd_mean').getInfo())


# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map