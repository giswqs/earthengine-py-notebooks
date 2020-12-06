# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Image/reduce_region.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Image/reduce_region.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Image/reduce_region.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Image.reduceRegion example
#
# Computes a simple reduction over a region of an image.  A reduction
# is any process that takes an arbitrary number of inputs (such as
# all the pixels of an image in a given region) and computes one or
# more fixed outputs.  The result is a dictionary that contains the
# computed values, which in this example is the maximum pixel value
# in the region.

# This example shows how to print the resulting dictionary to the
# console, which is useful when developing and debugging your
# scripts, but in a larger workflow you might instead use the
# Dicitionary.get() function to extract the values you need from the
# dictionary for use as inputs to other functions.

# The input image to reduce, in this case an SRTM elevation map.
image = ee.Image('CGIAR/SRTM90_V4')

# The region to reduce within.
poly = ee.Geometry.Rectangle([-109.05, 41, -102.05, 37])

# Reduce the image within the given region, using a reducer that
# computes the max pixel value.  We also specify the spatial
# resolution at which to perform the computation, in this case 200
# meters.
max = image.reduceRegion(**{
  'reducer': ee.Reducer.max(),
  'geometry': poly,
  'scale': 200
})

# Print the result (a Dictionary) to the console.
print(max.getInfo())


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map