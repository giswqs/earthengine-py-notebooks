'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Reducer/linear_regression_more.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Reducer/linear_regression_more.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Reducer/linear_regression_more.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Reducer/linear_regression_more.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map