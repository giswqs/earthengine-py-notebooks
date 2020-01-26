'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Reducer/convert_raster_to_vector.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Reducer/convert_raster_to_vector.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Reducer/convert_raster_to_vector.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Reducer/convert_raster_to_vector.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
</table>
'''

# %%
'''
## Install Earth Engine API
Install the [Earth Engine Python API](https://developers.google.com/earth-engine/python_install) and [geehydro](https://github.com/giswqs/geehydro). The **geehydro** Python package builds on the [folium](https://github.com/python-visualization/folium) package and implements several methods for displaying Earth Engine data layers, such as `Map.addLayer()`, `Map.setCenter()`, `Map.centerObject()`, and `Map.setOptions()`.
The magic command `%%capture` can be used to hide output from a specific cell.
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
if you are running this notebook for this first time or if you are getting an authentication error.  
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
# Load a Japan boundary from the Large Scale International Boundary dataset.
japan = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017') \
  .filter(ee.Filter.eq('country_na', 'Japan'))

# Load a 2012 nightlights image, clipped to the Japan border.
nl2012 = ee.Image('NOAA/DMSP-OLS/NIGHTTIME_LIGHTS/F182012') \
  .select('stable_lights') \
  .clipToCollection(japan)

# Define arbitrary thresholds on the 6-bit nightlights image.
zones = nl2012.gt(30).add(nl2012.gt(55)).add(nl2012.gt(62))
zones = zones.updateMask(zones.neq(0))

# Convert the zones of the thresholded nightlights to vectors.
vectors = zones.addBands(nl2012).reduceToVectors(**{
  'geometry': japan,
  'crs': nl2012.projection(),
  'scale': 1000,
  'geometryType': 'polygon',
  'eightConnected': False,
  'labelProperty': 'zone',
  'reducer': ee.Reducer.mean()
})

# Display the thresholds.
Map.setCenter(139.6225, 35.712, 9)
Map.addLayer(zones, {'min': 1, 'max': 3, 'palette': ['0000FF', '00FF00', 'FF0000']}, 'raster')

# Make a display image for the vectors, add it to the map.
display = ee.Image(0).updateMask(0).paint(vectors, '000000', 3)
Map.addLayer(display, {'palette': '000000'}, 'vectors')



# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map