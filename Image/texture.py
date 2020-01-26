'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Image/texture.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Image/texture.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Image/texture.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Image/texture.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map