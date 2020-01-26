'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Image/cumulative_cost_mapping.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Image/cumulative_cost_mapping.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Image/cumulative_cost_mapping.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Image/cumulative_cost_mapping.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# A rectangle representing Bangui, Central African Republic.
geometry = ee.Geometry.Rectangle([18.5229, 4.3491, 18.5833, 4.4066])

# Create a source image where the geometry is 1, everything else is 0.
sources = ee.Image().toByte().paint(geometry, 1)

# Mask the sources image with itself.
sources = sources.updateMask(sources)

# The cost data is generated from classes in ESA/GLOBCOVER.
cover = ee.Image('ESA/GLOBCOVER_L4_200901_200912_V2_3').select(0)

# Classes 60, 80, 110, 140 have cost 1.
# Classes 40, 90, 120, 130, 170 have cost 2.
# Classes 50, 70, 150, 160 have cost 3.
cost = \
  cover.eq(60).Or(cover.eq(80)).Or(cover.eq(110)).Or(cover.eq(140)) \
      .multiply(1).add(
  cover.eq(40).Or(cover.eq(90)).Or(cover.eq(120)).Or(cover.eq(130)) \
    .Or(cover.eq(170)) \
      .multiply(2).add(
  cover.eq(50).Or(cover.eq(70)).Or(cover.eq(150)).Or(cover.eq(160)) \
      .multiply(3)))

# Compute the cumulative cost to traverse the lAnd cover.
cumulativeCost = cost.cumulativeCost(**{
  'source': sources,
  'maxDistance': 80 * 1000 # 80 kilometers
})

# Display the results
Map.setCenter(18.71, 4.2, 9)
Map.addLayer(cover, {}, 'Globcover')
Map.addLayer(cumulativeCost, {'min': 0, 'max': 5e4}, 'accumulated cost')
Map.addLayer(geometry, {'color': 'FF0000'}, 'source geometry')


# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map