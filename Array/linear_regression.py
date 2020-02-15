'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Array/linear_regression.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Array/linear_regression.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Array/linear_regression.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Array/linear_regression.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
</table>
'''

# %%
'''
## Install Earth Engine API
Install the [Earth Engine Python API](https://developers.google.com/earth-engine/python_install) and [geehydro](https://github.com/giswqs/geehydro). The **geehydro** Python package builds on the [folium](https://github.com/python-visualization/folium) package and implements several methods for displaying Earth Engine data layers, such as `Map.addLayer()`, `Map.setCenter()`, `Map.centerObject()`, and `Map.setOptions()`.
The following script checks if the geehydro package has been installed. If not, it will install geehydro, which automatically install its dependencies, including earthengine-api and folium.
'''


# %%
import subprocess

try:
    import geehydro
except ImportError:
    print('geehydro package not installed. Installing ...')
    subprocess.check_call(["python", '-m', 'pip', 'install', 'geehydro'])

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
Authenticate and initialize Earth Engine API. You only need to authenticate the Earth Engine API once. 
'''


# %%
try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
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
# Simple regression of year versus NDVI.

# Define the start date and position to get images covering Montezuma Castle,
# Arizona, from 2000-2010.
start = '2000-01-01'
end = '2010-01-01'
lng = -111.83533
lat = 34.57499
region = ee.Geometry.Point(lng, lat)

# Filter to Landsat 7 images in the given time and place, filter to a regular
# time of year to avoid seasonal affects, and for each image create the bands
# we will regress on:
# 1. A 1, so the resulting array has a column of ones to capture the offset.
# 2. Fractional year past 2000-01-01.
# 3. NDVI.

def addBand(image):
    date = ee.Date(image.get('system:time_start'))
    yearOffset = date.difference(ee.Date(start), 'year')
    ndvi = image.normalizedDifference(['B4', 'B3'])
    return ee.Image(1).addBands(yearOffset).addBands(ndvi).toDouble()


images = ee.ImageCollection('LANDSAT/LE07/C01/T1') \
  .filterDate(start, end) \
  .filter(ee.Filter.dayOfYear(160, 240)) \
  .filterBounds(region) \
  .map(addBand) 
#     date = ee.Date(image.get('system:time_start'))
#     yearOffset = date.difference(ee.Date(start), 'year')
#     ndvi = image.normalizedDifference(['B4', 'B3'])
#     return ee.Image(1).addBands(yearOffset).addBands(ndvi).toDouble()
#   })

# Convert to an array. Give the axes names for more readable code.
array = images.toArray()
imageAxis = 0
bandAxis = 1

# Slice off the year and ndvi, and solve for the coefficients.
x = array.arraySlice(bandAxis, 0, 2)
y = array.arraySlice(bandAxis, 2)
fit = x.matrixSolve(y)

# Get the coefficient for the year, effectively the slope of the long-term
# NDVI trend.
slope = fit.arrayGet([1, 0])

Map.setCenter(lng, lat, 12)
Map.addLayer(slope, {'min': -0.03, 'max': 0.03}, 'Slope')



# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map