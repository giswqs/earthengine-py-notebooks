# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Reducer/linear_regression.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Reducer/linear_regression.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Reducer/linear_regression.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# This function adds a time band to the image.

def createTimeBand(image):
    return image.addBands(image.metadata('system:time_start').divide(1e18))

# createTimeBand = function(image) {
#   # Scale milliseconds by a large constant to avoid very small slopes
#   # in the linear regression output.
#   return image.addBands(image.metadata('system:time_start').divide(1e18))
# }

# Load the input image 'collection': projected climate data.
collection = ee.ImageCollection('NASA/NEX-DCP30_ENSEMBLE_STATS') \
  .filter(ee.Filter.eq('scenario', 'rcp85')) \
  .filterDate(ee.Date('2006-01-01'), ee.Date('2050-01-01')) \
  .map(createTimeBand)

# Reduce the collection with the linear fit reducer.
# Independent variable are followed by dependent variables.
linearFit = collection.select(['system:time_start', 'pr_mean']) \
  .reduce(ee.Reducer.linearFit())

# Display the results.
Map.setCenter(-100.11, 40.38, 5)
Map.addLayer(linearFit,
  {'min': 0, 'max': [-0.9, 8e-5, 1], 'bands': ['scale', 'offset', 'scale']}, 'fit')



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map