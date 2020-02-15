'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Gena/hillshade_and_water.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Gena/hillshade_and_water.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Gena/hillshade_and_water.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Gena/hillshade_and_water.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
from ee_plugin.contrib import palettes

dem = ee.Image("JAXA/ALOS/AW3D30_V1_1").select('MED')
dem = dem.updateMask(dem.gt(0))
palette = palettes.cb['Pastel1'][7]
#palette = ['black', 'white']
rgb = dem.visualize(**{'min': 0, 'max': 5000, 'palette': palette })
hsv = rgb.unitScale(0, 255).rgbToHsv()

extrusion = 30
weight = 0.7

hs = ee.Terrain.hillshade(dem.multiply(extrusion), 315, 35).unitScale(10, 250).resample('bicubic')

hs = hs.multiply(weight).add(hsv.select('value').multiply(1 - weight))
hsv = hsv.addBands(hs.rename('value'), ['value'], True)
rgb = hsv.hsvToRgb()

Map.addLayer(rgb, {}, 'ALOS DEM', True, 0.5)

water_occurrence = ( ee.Image("JRC/GSW1_0/GlobalSurfaceWater")
  .select('occurrence')
  .divide(100)
  .unmask(0)
  .resample('bicubic') )
  
palette = ["ffffcc","ffeda0","fed976","feb24c","fd8d3c","fc4e2a","e31a1c","bd0026","800026"][::-1][1:]

land = ee.Image("users/gena/land_polygons_image").mask()

Map.addLayer(water_occurrence.mask(water_occurrence.multiply(2).multiply(land)), {'min': 0, 'max': 1, 'palette': palette}, 'water occurrence', True)






# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map