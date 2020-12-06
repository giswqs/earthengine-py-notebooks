# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Image/edge_detection.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Image/edge_detection.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Image/edge_detection.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Load a Landsat 8 image, select the panchromatic band.
image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318').select('B8')

# Perform Canny edge detection and display the result.
canny = ee.Algorithms.CannyEdgeDetector(**{
  'image': image, 'threshold': 10, 'sigma': 1
})
Map.setCenter(-122.054, 37.7295, 10)
Map.addLayer(canny, {}, 'canny')

# Perform Hough transform of the Canny result and display.
hough = ee.Algorithms.HoughTransform(canny, 256, 600, 100)
Map.addLayer(hough, {}, 'hough')

# Load a Landsat 8 image, select the panchromatic band.
image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318').select('B8')
Map.addLayer(image, {'max': 12000})

# Define a "fat" Gaussian kernel.
fat = ee.Kernel.gaussian(**{
  'radius': 3,
  'sigma': 3,
  'units': 'pixels',
  'normalize': True,
  'magnitude': -1
})

# Define a "skinny" Gaussian kernel.
skinny = ee.Kernel.gaussian(**{
  'radius': 3,
  'sigma': 1,
  'units': 'pixels',
  'normalize': True,
})

# Compute a difference-of-Gaussians (DOG) kernel.
dog = fat.add(skinny)

# Compute the zero crossings of the second derivative, display.
zeroXings = image.convolve(dog).zeroCrossing()
Map.setCenter(-122.054, 37.7295, 10)
Map.addLayer(zeroXings.updateMask(zeroXings), {'palette': 'FF0000'}, 'zero crossings')



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map