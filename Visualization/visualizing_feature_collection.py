'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Visualization/visualizing_feature_collection.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Visualization/visualizing_feature_collection.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Visualization/visualizing_feature_collection.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Visualization/visualizing_feature_collection.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Load a FeatureCollection from a table dataset: 'RESOLVE' ecoregions.
ecoregions = ee.FeatureCollection('RESOLVE/ECOREGIONS/2017')

# Display as default and with a custom color.
Map.addLayer(ecoregions, {}, 'default display')
Map.addLayer(ecoregions, {'color': 'FF0000'}, 'colored')


Map.addLayer(ecoregions.draw(**{'color': '006600', 'strokeWidth': 5}), {}, 'drawn')


# Create an empty image into which to paint the features, cast to byte.
empty = ee.Image().byte()

# Paint all the polygon edges with the same number and 'width', display.
outline = empty.paint(**{
  'featureCollection': ecoregions,
  'color': 1,
  'width': 3
})
Map.addLayer(outline, {'palette': 'FF0000'}, 'edges')


# Paint the edges with different colors, display.
outlines = empty.paint(**{
  'featureCollection': ecoregions,
  'color': 'BIOME_NUM',
  'width': 4
})
palette = ['FF0000', '00FF00', '0000FF']
Map.addLayer(outlines, {'palette': palette, 'max': 14}, 'different color edges')


# Paint the edges with different colors and 'width's.
outlines = empty.paint(**{
  'featureCollection': ecoregions,
  'color': 'BIOME_NUM',
  'width': 'NNH'
})
Map.addLayer(outlines, {'palette': palette, 'max': 14}, 'different color, width edges')


# Paint the interior of the polygons with different colors.
fills = empty.paint(**{
  'featureCollection': ecoregions,
  'color': 'BIOME_NUM',
})
Map.addLayer(fills, {'palette': palette, 'max': 14}, 'colored fills')


# Paint both the fill and the edges.
filledOutlines = empty.paint(ecoregions, 'BIOME_NUM').paint(ecoregions, 0, 2)
Map.addLayer(filledOutlines, {'palette': ['000000'] + palette, 'max': 14}, 'edges and fills')



# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map