# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Gena/contrib/utils-hillshadeRgb.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Gena/contrib/utils-hillshadeRgb.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Gena/contrib/utils-hillshadeRgb.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map