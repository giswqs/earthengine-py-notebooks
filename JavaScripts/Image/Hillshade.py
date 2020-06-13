# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/JavaScripts/Image/Hillshade.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/JavaScripts/Image/Hillshade.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/JavaScripts/Image/Hillshade.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
import math

# Hillshade example.  This is a demonstration of computing
# a hillshade from terrain data and displaying multiple
# layers based on multiple view geometries.  Hillshade
# creation is also provided by ee.Terrain.hillshade().

# Define a function to convert from degrees to radians.
def radians(img):
  return img.toFloat().multiply(math.pi).divide(180)


# Define a function to compute a hillshade from terrain data
# for the given sun azimuth and elevation.
def hillshade(az, ze, slope, aspect):
  # Convert angles to radians.
  azimuth = radians(ee.Image(az))
  zenith = radians(ee.Image(ze))
  # Note that methods on images are needed to do the computation.
  # i.e. JavaScript operators (e.g. +, -, /, *) do not work on images.
  # The following implements:
  # Hillshade = cos(Azimuth - Aspect) * sin(Slope) * sin(Zenith) + \
  #     cos(Zenith) * cos(Slope)
  return azimuth.subtract(aspect).cos() \
    .multiply(slope.sin()) \
    .multiply(zenith.sin()) \
    .add(
      zenith.cos().multiply(slope.cos()))


# Compute terrain meaasures from the SRTM DEM.
terrain = ee.Algorithms.Terrain(ee.Image('CGIAR/SRTM90_V4'))
slope = radians(terrain.select('slope'))
aspect = radians(terrain.select('aspect'))

# For loops are needed for control-flow operations on client-side
# operations.  Here Map.addLayer() is a client operation that needs
# to be performed in a for loop.  In general, avoid for loops
# for any server-side operation.
Map.setCenter(-121.767, 46.852, 11)
for i in range(0, 360, 60):
  Map.addLayer(hillshade(i, 60, slope, aspect), {}, i + ' deg')



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map