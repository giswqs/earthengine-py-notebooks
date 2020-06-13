# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/JavaScripts/Arrays/LinearRegression.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/JavaScripts/Arrays/LinearRegression.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/JavaScripts/Arrays/LinearRegression.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
</table>
"""

# %%
"""
## Install Earth Engine API and geemap
Install the [Earth Engine Python API](https://developers.google.com/earth-engine/python_install) and [geemap](https://github.com/giswqs/geemap). The **geemap** Python package is built upon the [ipyleaflet](https://github.com/jupyter-widgets/ipyleaflet) and [folium](https://github.com/python-visualization/folium) packages and implements several methods for interacting with Earth Engine data layers, such as `Map.addLayer()`, `Map.setCenter()`, and `Map.centerObject()`.
The following script checks if the geemap package has been installed. If not, it will install geemap, which automatically installs its [dependencies](https://github.com/giswqs/geemap#dependencies), including earthengine-api, folium, and ipyleaflet.

**Important note**: A key difference between folium and ipyleaflet is that ipyleaflet is built upon ipywidgets and allows bidirectional communication between the front-end and the backend enabling the use of the map to capture user input, while folium is meant for displaying static data only ([source](https://blog.jupyter.org/interactive-gis-in-jupyter-with-ipyleaflet-52f9657fa7a)). Note that [Google Colab](https://colab.research.google.com/) currently does not support ipyleaflet ([source](https://github.com/googlecolab/colabtools/issues/60#issuecomment-596225619)). Therefore, if you are using geemap with Google Colab, you should use [`import geemap.eefolium`](https://github.com/giswqs/geemap/blob/master/geemap/eefolium.py). If you are using geemap with [binder](https://mybinder.org/) or a local Jupyter notebook server, you can use [`import geemap`](https://github.com/giswqs/geemap/blob/master/geemap/geemap.py), which provides more functionalities for capturing user input (e.g., mouse-clicking and moving).
"""

# %%
# Installs geemap package
import subprocess

try:
    import geemap
except ImportError:
    print('geemap package not installed. Installing ...')
    subprocess.check_call(["python", '-m', 'pip', 'install', 'geemap'])

# Checks whether this notebook is running on Google Colab
try:
    import google.colab
    import geemap.eefolium as geemap
except:
    import geemap

# Authenticates and initializes Earth Engine
import ee

try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize()  

# %%
"""
## Create an interactive map 
The default basemap is `Google MapS`. [Additional basemaps](https://github.com/giswqs/geemap/blob/master/geemap/basemaps.py) can be added using the `Map.add_basemap()` function. 
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
images = ee.ImageCollection('LANDSAT/LE07/C01/T1') \
  .filterDate(start, end) \
  .filter(ee.Filter.dayOfYear(160, 240)) \
  .filterBounds(region)

def func_mrj(image):
    date = ee.Date(image.get('system:time_start'))
    yearOffset = date.difference(ee.Date(start), 'year')
    ndvi = image.normalizedDifference(['B4', 'B3'])
    return ee.Image(1).addBands(yearOffset).addBands(ndvi).toDouble() \
  .map(func_mrj)







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
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map