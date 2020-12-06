# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Image/hsv_pan_sharpen.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Image/hsv_pan_sharpen.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Image/hsv_pan_sharpen.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# There are many fine places to look here is one.  Comment
# this out if you want to twiddle knobs while panning around.
Map.setCenter(-61.61625, -11.64273, 14)

# Grab a sample L7 image and pull out the RGB and pan bands
# in the range (0, 1).  (The range of the pan band values was
# chosen to roughly match the other bands.)
image1 = ee.Image('LANDSAT/LE7/LE72300681999227EDC00')

rgb = image1.select('B3', 'B2', 'B1').unitScale(0, 255)
gray = image1.select('B8').unitScale(0, 155)

# Convert to HSV, swap in the pan band, and convert back to RGB.
huesat = rgb.rgbToHsv().select('hue', 'saturation')
upres = ee.Image.cat(huesat, gray).hsvToRgb()

# Display before and after layers using the same vis parameters.
visparams = {'min': [.15, .15, .25], 'max': [1, .9, .9], 'gamma': 1.6}
Map.addLayer(rgb, visparams, 'Orignal')
Map.addLayer(upres, visparams, 'Pansharpened')


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map