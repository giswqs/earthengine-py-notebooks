'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/FeatureCollection/geometric_operations.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/FeatureCollection/geometric_operations.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=FeatureCollection/geometric_operations.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/FeatureCollection/geometric_operations.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Create two circular geometries.
poly1 = ee.Geometry.Point([-50, 30]).buffer(1e6)
poly2 = ee.Geometry.Point([-40, 30]).buffer(1e6)

# Display polygon 1 in red and polygon 2 in blue.
Map.setCenter(-45, 30)
Map.addLayer(poly1, {'color': 'FF0000'}, 'poly1')
Map.addLayer(poly2, {'color': '0000FF'}, 'poly2')

# Compute the intersection, display it in blue.
intersection = poly1.intersection(poly2, ee.ErrorMargin(1))
Map.addLayer(intersection, {'color': '00FF00'}, 'intersection')

# Compute the union, display it in magenta.
union = poly1.union(poly2, ee.ErrorMargin(1))
Map.addLayer(union, {'color': 'FF00FF'}, 'union')

# Compute the difference, display in yellow.
diff1 = poly1.difference(poly2, ee.ErrorMargin(1))
Map.addLayer(diff1, {'color': 'FFFF00'}, 'diff1')

# Compute symmetric difference, display in black.
symDiff = poly1.symmetricDifference(poly2, ee.ErrorMargin(1))
Map.addLayer(symDiff, {'color': '000000'}, 'symmetric difference')



# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map