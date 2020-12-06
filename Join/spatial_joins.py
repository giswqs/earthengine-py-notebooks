# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Join/spatial_joins.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Join/spatial_joins.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Join/spatial_joins.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Load a primary 'collection': protected areas (Yosemite National Park).
primary = ee.FeatureCollection("WCMC/WDPA/current/polygons") \
  .filter(ee.Filter.eq('NAME', 'Yosemite National Park'))

# Load a secondary 'collection': power plants.
powerPlants = ee.FeatureCollection('WRI/GPPD/power_plants')

# Define a spatial filter, with distance 100 km.
distFilter = ee.Filter.withinDistance(**{
  'distance': 100000,
  'leftField': '.geo',
  'rightField': '.geo',
  'maxError': 10
})

# Define a saveAll join.
distSaveAll = ee.Join.saveAll(**{
  'matchesKey': 'points',
  'measureKey': 'distance'
})

# Apply the join.
spatialJoined = distSaveAll.apply(primary, powerPlants, distFilter)

# Print the result.
# print(spatialJoined.getInfo())
Map.centerObject(spatialJoined, 10)
Map.addLayer(ee.Image().paint(spatialJoined, 1, 3), {}, 'Spatial Joined')


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map