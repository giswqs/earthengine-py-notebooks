# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Algorithms/CloudMasking/modis_surface_reflectance_qa_band.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Algorithms/CloudMasking/modis_surface_reflectance_qa_band.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Algorithms/CloudMasking/modis_surface_reflectance_qa_band.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Modis Cloud Masking example.
# Calculate how frequently a location is labeled as clear (i.e. non-cloudy)
# according to the "internal cloud algorithm flag" of the MODIS "state 1km"
# QA band.

# A function to mask out pixels that did not have observations.
# maskEmptyPixels = function(image) {
def maskEmptyPixels(image):
  # Find pixels that had observations.
  withObs = image.select('num_observations_1km').gt(0)
  return image.updateMask(withObs)
# }

# A function to mask out cloudy pixels.
# maskClouds = function(image) {
def maskClouds(image):
  # Select the QA band.
  QA = image.select('state_1km')
  # Make a mask to get bit 10, the internal_cloud_algorithm_flag bit.
  bitMask = 1 << 10
  # Return an image masking out cloudy areas.
  return image.updateMask(QA.bitwiseAnd(bitMask).eq(0))
# }

# Start with an image collection for a 1 month period.
# and mask out areas that were not observed.
collection = ee.ImageCollection('MODIS/006/MOD09GA') \
        .filterDate('2010-04-01', '2010-05-01') \
        .map(maskEmptyPixels)

# Get the total number of potential observations for the time interval.
totalObsCount = collection \
        .select('num_observations_1km') \
        .count()

# Map the cloud masking function over the collection.
collectionCloudMasked = collection.map(maskClouds)

# Get the total number of observations for non-cloudy pixels for the time
# interval.  The result is unmasked to set to unity so that all locations
# have counts, and the ratios later computed have values everywhere.
clearObsCount = collectionCloudMasked \
        .select('num_observations_1km') \
        .count() \
        .unmask(0)

Map.addLayer(
    collectionCloudMasked.median(),
    {'bands': ['sur_refl_b01', 'sur_refl_b04', 'sur_refl_b03'],
     'gain': 0.07,
     'gamma': 1.4
    },
    'median of masked collection'
  )
Map.addLayer(
    totalObsCount,
    {'min': 84, 'max': 92},
    'count of total observations',
    False
  )
Map.addLayer(
    clearObsCount,
    {'min': 0, 'max': 90},
    'count of clear observations',
    False
  )
Map.addLayer(
    clearObsCount.toFloat().divide(totalObsCount),
    {'min': 0, 'max': 1},
    'ratio of clear to total observations'
  )




# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map