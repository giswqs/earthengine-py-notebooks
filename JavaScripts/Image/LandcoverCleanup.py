# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/JavaScripts/Image/LandcoverCleanup.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/JavaScripts/Image/LandcoverCleanup.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/JavaScripts/Image/LandcoverCleanup.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
</table>
"""

# %%
"""
## Install Earth Engine API and geemap
Install the [Earth Engine Python API](https://developers.google.com/earth-engine/python_install) and [geemap](https://github.com/giswqs/geemap). The **geemap** Python package is built upon the [ipyleaflet](https://github.com/jupyter-widgets/ipyleaflet) and [folium](https://github.com/python-visualization/folium) packages and implements several methods for interacting with Earth Engine data layers, such as `Map.addLayer()`, `Map.setCenter()`, and `Map.centerObject()`.
The following script checks if the geemap package has been installed. If not, it will install geemap, which automatically installs its [dependencies](https://github.com/giswqs/geemap#dependencies), including earthengine-api, folium, and ipyleaflet.

**Important note**: A key difference between folium and ipyleaflet is that ipyleaflet is built upon ipywidgets and allows bidirectional communication between the front-end and the backend enabling the use of the map to capture user input, while folium is meant for displaying static data only ([source](https://blog.jupyter.org/interactive-gis-in-jupyter-with-ipyleaflet-52f9657fa7a)). Note that [Google Colab](https://colab.research.google.com/) currently does not support ipyleaflet ([source](https://github.com/googlecolab/colabtools/issues/60#issuecomment-596225619)). Therefore, if you are using geemap with Google Colab, you should use [`import geemap.eefolium`](https://github.com/giswqs/geemap/blob/master/geemap/eefolium.py). If you are using geemap with [binder](https://mybinder.org/) or a local Jupyter notebook server, you can use [`import geemap`](https://github.com/giswqs/geemap/blob/master/geemap/geemap.py), which provides more functionalities for capturing user input (e.g., mouse-clicking and moving).
"""

# %%
# Installs geemap package
import subprocess

try:
    import geemap
except ImportError:
    print('geemap package not installed. Installing ...')
    subprocess.check_call(["python", '-m', 'pip', 'install', 'geemap'])

# Checks whether this notebook is running on Google Colab
try:
    import google.colab
    import geemap.eefolium as geemap
except:
    import geemap

# Authenticates and initializes Earth Engine
import ee

try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize()  

# %%
"""
## Create an interactive map 
The default basemap is `Google MapS`. [Additional basemaps](https://github.com/giswqs/geemap/blob/master/geemap/basemaps.py) can be added using the `Map.add_basemap()` function. 
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
# Morphological processing of land cover.  This example
# includes spatial smoothing (neighborhood mode) followed by
# dilation, erosion and dilation again.  Reprojection is
# used to force these operations to be performed at the
# native scale of the input (rather than variable pixel
# sizes based on zoom level).

# Force projection of 500 meters/pixel, which is the native MODIS resolution.
SCALE = 500

# Load a 2001 MODIS land cover image.
image1 = ee.Image('MODIS/051/MCD12Q1/2001_01_01')
# Select the classification band of interest.
image2 = image1.select(['Land_Cover_Type_1'])
# Reproject to WGS84 to force the image to be reprojected on load.
# This is just for display purposes, to visualize the input to
# the following operations.  The next reproject is sufficient
# to force the computation to occur at native scale.
image3 = image2.reproject('EPSG:4326', {}, SCALE)
# Smooth with a mode filter.
image4 = image3.focal_mode()
# Use erosion and dilation to get rid of small islands.
image5 = image4.focal_max(3).focal_min(5).focal_max(3)
# Reproject to force the operations to be performed at SCALE.
image6 = image5.reproject('EPSG:4326', {}, SCALE)

# Define display paramaters with appropriate colors for the MODIS
# land cover classification image.
PALETTE = [
    'aec3d4', # water
    '152106', '225129', '369b47', '30eb5b', '387242', # forest
    '6a2325', 'c3aa69', 'b76031', 'd9903d', '91af40', # shrub, grass, savannah
    '111149', # wetlands
    'cdb33b', # croplands
    'cc0013', # urban
    '33280d', # crop mosaic
    'd7cdcc', # snow and ice
    'f7e084', # barren
    '6f6f6f'  # tundra
].join(',')

vis_params = {'min': 0, 'max': 17, 'palette': PALETTE}

# Display each step of the computation.
Map.setCenter(-113.41842, 40.055489, 6)
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