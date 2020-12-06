# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Image/texture.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Image/texture.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Image/texture.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
import math

# Load a high-resolution NAIP image.
image = ee.Image('USDA/NAIP/DOQQ/m_3712213_sw_10_1_20140613')

# Zoom to San Francisco, display.
Map.setCenter(-122.466123, 37.769833, 17)
Map.addLayer(image, {'max': 255}, 'image')

# Get the NIR band.
nir = image.select('N')

# Define a neighborhood with a kernel.
square = ee.Kernel.square(**{'radius': 4})

# Compute entropy and display.
entropy = nir.entropy(square)
Map.addLayer(entropy,
             {'min': 1, 'max': 5, 'palette': ['0000CC', 'CC0000']},
             'entropy')

# Compute the gray-level co-occurrence matrix (GLCM), get contrast.
glcm = nir.glcmTexture(**{'size': 4})
contrast = glcm.select('N_contrast')
Map.addLayer(contrast,
             {'min': 0, 'max': 1500, 'palette': ['0000CC', 'CC0000']},
             'contrast')

# Create a list of weights for a 9x9 kernel.
list = [1, 1, 1, 1, 1, 1, 1, 1, 1]
# The center of the kernel is zero.
centerList = [1, 1, 1, 1, 0, 1, 1, 1, 1]
# Assemble a list of lists: the 9x9 kernel weights as a 2-D matrix.
lists = [list, list, list, list, centerList, list, list, list, list]
# Create the kernel from the weights.
# Non-zero weights represent the spatial neighborhood.
kernel = ee.Kernel.fixed(9, 9, lists, -4, -4, False)

# Convert the neighborhood into multiple bands.
neighs = nir.neighborhoodToBands(kernel)

# Compute local Geary's C, a measure of spatial association.
gearys = nir.subtract(neighs).pow(2).reduce(ee.Reducer.sum()) \
             .divide(math.pow(9, 2))
Map.addLayer(gearys,
             {'min': 20, 'max': 2500, 'palette': ['0000CC', 'CC0000']},
             "Geary's C")



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map