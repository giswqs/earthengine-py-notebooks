# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Reducer/linear_regression_more.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Reducer/linear_regression_more.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Reducer/linear_regression_more.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
    import geemap.eefolium as emap
except:
    import geemap as emap

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
The default basemap is `Google Satellite`. [Additional basemaps](https://github.com/giswqs/geemap/blob/master/geemap/geemap.py#L13) can be added using the `Map.add_basemap()` function. 
"""

# %%
Map = emap.Map(center=[40,-100], zoom=4)
Map.add_basemap('ROADMAP') # Add Google Map
Map

# %%
"""
## Add Earth Engine Python script 
"""

# %%
# Add Earth Engine dataset
# This function adds a time band to the image.

def createTimeBand(image):
    return image.addBands(image.metadata('system:time_start').divide(1e18))

# createTimeBand = function(image) {
#   # Scale milliseconds by a large constant.
#   return image.addBands(image.metadata('system:time_start').divide(1e18))
# }

# This function adds a constant band to the image.
def createConstantBand(image):
    return ee.Image(1).addBands(image)
# createConstantBand = function(image) {
#   return ee.Image(1).addBands(image)
# }

# Load the input image 'collection': projected climate data.
collection = ee.ImageCollection('NASA/NEX-DCP30_ENSEMBLE_STATS') \
  .filterDate(ee.Date('2006-01-01'), ee.Date('2099-01-01')) \
  .filter(ee.Filter.eq('scenario', 'rcp85')) \
  .map(createTimeBand) \
  .map(createConstantBand) \
  .select(['constant', 'system:time_start', 'pr_mean', 'tasmax_mean'])

# Compute ordinary least squares regression coefficients.
linearRegression = collection.reduce(
  ee.Reducer.linearRegression(**{
    'numX': 2,
    'numY': 2
}))

# Compute robust linear regression coefficients.
robustLinearRegression = collection.reduce(
  ee.Reducer.robustLinearRegression(**{
    'numX': 2,
    'numY': 2
}))

# The results are array images that must be flattened for display.
# These lists label the information along each axis of the arrays.
bandNames = [['constant', 'time'], # 0-axis variation.
                 ['precip', 'temp']] # 1-axis variation.

# Flatten the array images to get multi-band images according to the labels.
lrImage = linearRegression.select(['coefficients']).arrayFlatten(bandNames)
rlrImage = robustLinearRegression.select(['coefficients']).arrayFlatten(bandNames)

# Display the OLS results.
Map.setCenter(-100.11, 40.38, 5)
Map.addLayer(lrImage,
  {'min': 0, 'max': [-0.9, 8e-5, 1], 'bands': ['time_precip', 'constant_precip', 'time_precip']}, 'OLS')

# Compare the results at a specific point:
print('OLS estimates:', lrImage.reduceRegion(**{
  'reducer': ee.Reducer.first(),
  'geometry': ee.Geometry.Point([-96.0, 41.0]),
  'scale': 1000
}).getInfo())

print('Robust estimates:', rlrImage.reduceRegion(**{
  'reducer': ee.Reducer.first(),
  'geometry': ee.Geometry.Point([-96.0, 41.0]),
  'scale': 1000
}).getInfo())



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map