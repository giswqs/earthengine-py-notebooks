'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/NAIP/ndwi.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/NAIP/ndwi.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=NAIP/ndwi.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/NAIP/ndwi.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
collection = ee.ImageCollection('USDA/NAIP/DOQQ')
fromFT = ee.FeatureCollection('ft:1CLldB-ULPyULBT2mxoRNv7enckVF0gCQoD2oH7XP')
polys = fromFT.geometry()
centroid = polys.centroid()
lng, lat = centroid.getInfo()['coordinates']
# print("lng = {}, lat = {}".format(lng, lat))

# lng_lat = ee.Geometry.Point(lng, lat)
naip = collection.filterBounds(polys)
naip_2015 = naip.filterDate('2015-01-01', '2015-12-31')
ppr = naip_2015.mosaic().clip(polys)

# print(naip_2015.size().getInfo())   # count = 120
vis = {'bands': ['N', 'R', 'G']}
Map.setCenter(lng, lat, 10)
# Map.addLayer(naip_2015,vis)
Map.addLayer(ppr,vis)
# Map.addLayer(fromFT)

ndwi = ppr.normalizedDifference(['G', 'N'])
ndwiViz = {'min': 0, 'max': 1, 'palette': ['00FFFF', '0000FF']}
ndwiMasked = ndwi.updateMask(ndwi.gte(0.05))
ndwi_bin = ndwiMasked.gt(0)
Map.addLayer(ndwiMasked, ndwiViz)

patch_size = ndwi_bin.connectedPixelCount(256, True)
# Map.addLayer(patch_size)

patch_id = ndwi_bin.connectedComponents(ee.Kernel.plus(1), 256)
Map.addLayer(patch_id)

# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map