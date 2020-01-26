'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Gena/contrib/utils-hillshadeRgb.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Gena/contrib/utils-hillshadeRgb.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Gena/contrib/utils-hillshadeRgb.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Gena/contrib/utils-hillshadeRgb.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
from ee_plugin.contrib import utils, palettes

dem = ee.Image("AHN/AHN2_05M_RUW") \
  .resample('bicubic') \
  .focal_max(0.5, 'circle', 'meters') \
  .convolve(ee.Kernel.gaussian(0.5, 0.25, 'meters'))

# See https://github.com/gee-community/ee-palettes 
# for the full list of supported color palettes
# palette = palettes.crameri['lisbon'][50]
palette = palettes.crameri['oleron'][50]
# palette = palettes.crameri['roma'][50][::-1] # reversed
# palette = palettes.crameri['batlow'][50]

demRGB = dem.visualize(**{ 'min': -5, 'max': 5, 'palette': palette })
Map.addLayer(demRGB , {}, 'DEM (RGB)', False)

weight = 0.5 # hillshade vs RGB intensity (0 - flat, 1 - HS)
exaggeration = 3 # vertical exaggeration
azimuth = 300 # Sun azimuth
zenith = 25 # Sun elevation
brightness = -0.05 # 0 - default
contrast = 0.05 # 0 - default
saturation = 0.8 # 1 - default
castShadows = False

# no shadows
rgb = utils.hillshadeRGB(demRGB, dem, weight, exaggeration,
    azimuth, zenith, contrast, brightness, saturation, castShadows)
Map.addLayer(rgb, {}, 'DEM (hillshade)', False)

# with shadows
castShadows = True
rgb = utils.hillshadeRGB(demRGB, dem, weight, exaggeration, 
    azimuth, zenith, contrast, brightness, saturation, castShadows)
Map.addLayer(rgb, {}, 'DEM (hillshade, shadows)')


# Map.setCenter(4.407, 52.177, 18)


# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map