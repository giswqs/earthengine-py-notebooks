# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Image/connected_pixel_count.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Image/connected_pixel_count.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Image/connected_pixel_count.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Image.ConnectedPixelCount example.

# Split pixels of band 01 into "bright" (arbitrarily defined as
# reflectance > 0.3) and "dim". Highlight small (<30 pixels)
# standalone islands of "bright" or "dim" type.
img = ee.Image('MODIS/006/MOD09GA/2012_03_09') \
              .select('sur_refl_b01') \
              .multiply(0.0001)

# Create a threshold image.
bright = img.gt(0.3)

# Compute connected pixel counts stop searching for connected pixels
# once the size of the connected neightborhood reaches 30 pixels, and
# use 8-connected rules.
conn = bright.connectedPixelCount(**{
  'maxSize': 30,
  'eightConnected': True
})

# Make a binary image of small clusters.
smallClusters = conn.lt(30)

Map.setCenter(-107.24304, 35.78663, 8)
Map.addLayer(img, {'min': 0, 'max': 1}, 'original')
Map.addLayer(smallClusters.updateMask(smallClusters),
         {'min': 0, 'max': 1, 'palette': 'FF0000'}, 'cc')


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map