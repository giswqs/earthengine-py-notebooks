# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Datasets/Vectors/usgs_watershed_boundary.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Datasets/Vectors/usgs_watershed_boundary.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Datasets/Vectors/usgs_watershed_boundary.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
dataset = ee.FeatureCollection('USGS/WBD/2017/HUC02')
styleParams = {
  'fillColor': '000070',
  'color': '0000be',
  'width': 3.0,
}
regions = dataset.style(**styleParams)
Map.setCenter(-96.8, 40.43, 4)
Map.addLayer(regions, {}, 'USGS/WBD/2017/HUC02')


dataset = ee.FeatureCollection('USGS/WBD/2017/HUC04')
styleParams = {
  'fillColor': '5885E3',
  'color': '0000be',
  'width': 3.0,
}
subregions = dataset.style(**styleParams)
Map.setCenter(-110.904, 36.677, 7)
Map.addLayer(subregions, {}, 'USGS/WBD/2017/HUC04')


dataset = ee.FeatureCollection('USGS/WBD/2017/HUC06')
styleParams = {
  'fillColor': '588593',
  'color': '587193',
  'width': 3.0,
}
basins = dataset.style(**styleParams)
Map.setCenter(-96.8, 40.43, 7)
Map.addLayer(basins, {}, 'USGS/WBD/2017/HUC06')


dataset = ee.FeatureCollection('USGS/WBD/2017/HUC08')
styleParams = {
  'fillColor': '2E8593',
  'color': '587193',
  'width': 2.0,
}
subbasins = dataset.style(**styleParams)
Map.setCenter(-96.8, 40.43, 8)
Map.addLayer(subbasins, {}, 'USGS/WBD/2017/HUC08')


dataset = ee.FeatureCollection('USGS/WBD/2017/HUC10')
styleParams = {
  'fillColor': '2E85BB',
  'color': '2E5D7E',
  'width': 1.0,
}
watersheds = dataset.style(**styleParams)
Map.setCenter(-96.8, 40.43, 9)
Map.addLayer(watersheds, {}, 'USGS/WBD/2017/HUC10')


dataset = ee.FeatureCollection('USGS/WBD/2017/HUC12')
styleParams = {
  'fillColor': '2E85BB',
  'color': '2E5D7E',
  'width': 0.1,
}
subwatersheds = dataset.style(**styleParams)
Map.setCenter(-96.8, 40.43, 10)
Map.addLayer(subwatersheds, {}, 'USGS/WBD/2017/HUC12')


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map