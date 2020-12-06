# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Image/landcover_cleanup.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Image/landcover_cleanup.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Image/landcover_cleanup.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
Map.setCenter(-113.41842, 40.055489, 6)

# Force projection of 500 meters/pixel, which is the native MODIS resolution.
VECTORIZATION_SCALE = 500

image1 = ee.Image('MCD12Q1/MCD12Q1_005_2001_01_01')
image2 = image1.select(['Land_Cover_Type_1'])
image3 = image2.reproject('EPSG:4326', None, 500)
image4 = image3.focal_mode()
image5 = image4.focal_max(3).focal_min(5).focal_max(3)
image6 = image5.reproject('EPSG:4326', None, 500)

PALETTE = [
    'aec3d4',  # water
    '152106', '225129', '369b47', '30eb5b', '387242',  # forest
    '6a2325', 'c3aa69', 'b76031', 'd9903d', '91af40',  # shrub, grass, savannah
    '111149',  # wetlands
    'cdb33b',  # croplands
    'cc0013',  # urban
    '33280d',  # crop mosaic
    'd7cdcc',  # snow and ice
    'f7e084',  # barren
    '6f6f6f'   # tundra
    ]

vis_params = {'min': 0, 'max': 17, 'palette': PALETTE}

Map.addLayer(image2, vis_params, 'IGBP classification')
Map.addLayer(image3, vis_params, 'Reprojected')
Map.addLayer(image4, vis_params, 'Mode')
Map.addLayer(image5, vis_params, 'Smooth')
Map.addLayer(image6, vis_params, 'Smooth')


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map