'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Visualization/image_thumbanil.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Visualization/image_thumbanil.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Visualization/image_thumbanil.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Visualization/image_thumbanil.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Fetch a digital elevation model.
image = ee.Image('CGIAR/SRTM90_V4')

# Request a default thumbnail of the DEM with defined linear stretch.
# Set masked pixels (ocean) to 1000 so they map as gray.
thumbnail1 = image.unmask(1000).getThumbURL({
  'min': 0,
  'max': 3000
})
print('Thumbnail:', thumbnail1)

# # Specify region by GeoJSON, define palette, set size of the larger aspect dimension.
# thumbnail2 = image.getThumbURL({
#   'min': 0,
#   'max': 3000,
#   'palette': ['00A600','63C600','E6E600','E9BD3A','ECB176','EFC2B3','F2F2F2'],
#   'dimensions': 500,
#   'region': ee.Geometry.Rectangle([-84.6, -55.9, -32.9, 15.7]),
# })
# print('GeoJSON region, palette, and max dimension:', thumbnail2)

# # Specify region by list of points and set display CRS as Web Mercator.
# thumbnail3 = image.getThumbURL({
#   'min': 0,
#   'max': 3000,
#   'palette': ['00A600','63C600','E6E600','E9BD3A','ECB176','EFC2B3','F2F2F2'],
#   'region': [[-84.6, 15.7], [-84.6, -55.9], [-32.9, -55.9]],
#   'crs': 'EPSG:3857'
# })
# print('Linear ring region and specified crs', thumbnail3)

# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map