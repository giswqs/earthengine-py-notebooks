'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Algorithms/CloudMasking/modis_surface_reflectance_qa_band.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Algorithms/CloudMasking/modis_surface_reflectance_qa_band.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Algorithms/CloudMasking/modis_surface_reflectance_qa_band.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Algorithms/CloudMasking/modis_surface_reflectance_qa_band.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map