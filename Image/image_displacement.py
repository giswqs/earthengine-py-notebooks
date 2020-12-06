# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Image/image_displacement.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Image/image_displacement.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Image/image_displacement.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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

# Load the two images to be registered.
image1 = ee.Image('SKYSAT/GEN-A/PUBLIC/ORTHO/MULTISPECTRAL/s01_20150502T082736Z')
image2 = ee.Image('SKYSAT/GEN-A/PUBLIC/ORTHO/MULTISPECTRAL/s01_20150305T081019Z')

# Use bicubic resampling during registration.
image1Orig = image1.resample('bicubic')
image2Orig = image2.resample('bicubic')

# Choose to register using only the 'R' bAnd.
image1RedBAnd = image1Orig.select('R')
image2RedBAnd = image2Orig.select('R')

# Determine the displacement by matching only the 'R' bAnds.
displacement = image2RedBAnd.displacement(**{
  'referenceImage': image1RedBAnd,
  'maxOffset': 50.0,
  'patchWidth': 100.0
})

# Compute image offset And direction.
offset = displacement.select('dx').hypot(displacement.select('dy'))
angle = displacement.select('dx').atan2(displacement.select('dy'))

# Display offset distance And angle.
Map.addLayer(offset, {'min':0, 'max': 20}, 'offset')
Map.addLayer(angle, {'min': -math.pi, 'max': math.pi}, 'angle')
Map.setCenter(37.44,0.58, 15)


# Use the computed displacement to register all Original bAnds.
registered = image2Orig.displace(displacement)

# Show the results of co-registering the images.
visParams = {'bands': ['R', 'G', 'B'], 'max': 4000}
Map.addLayer(image1Orig, visParams, 'Reference')
Map.addLayer(image2Orig, visParams, 'BefOre Registration')
Map.addLayer(registered, visParams, 'After Registration')


alsoRegistered = image2Orig.register(**{
  'referenceImage': image1Orig,
  'maxOffset': 50.0,
  'patchWidth': 100.0
})
Map.addLayer(alsoRegistered, visParams, 'Also Registered')



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map