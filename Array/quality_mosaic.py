# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Array/quality_mosaic.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Array/quality_mosaic.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Array/quality_mosaic.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Array-based quality mosaic.

# Returns a mosaic built by sorting each stack of pixels by the first band
# in descending order, and taking the highest quality pixel.
# function qualityMosaic(bands) {
def qualityMosaic(bands):
  # Convert to an array, and declare names for the axes and indices along the
  # band axis.
  array = bands.toArray()
  imageAxis = 0
  bandAxis = 1
  qualityIndex = 0
  valuesIndex = 1

  # Slice the quality and values off the main array, and sort the values by the
  # quality in descending order.
  quality = array.arraySlice(bandAxis, qualityIndex, qualityIndex + 1)
  values = array.arraySlice(bandAxis, valuesIndex)
  valuesByQuality = values.arraySort(quality.multiply(-1))

  # Get an image where each pixel is the array of band values where the quality
  # band is greatest. Note that while the array is 2-D, the first axis is
  # length one.
  best = valuesByQuality.arraySlice(imageAxis, 0, 1)

  # Project the best 2D array down to a single dimension, and convert it back
  # to a regular scalar image by naming each position along the axis. Note we
  # provide the original band names, but slice off the first band since the
  # quality band is not part of the result. Also note to get at the band names,
  # we have to do some kind of reduction, but it won't really calculate pixels
  # if we only access the band names.
  bandNames = bands.min().bandNames().slice(1)
  return best.arrayProject([bandAxis]).arrayFlatten([bandNames])
# }

# Load the l7_l1t collection for the year 2000, and make sure the first band
# is our quality measure, in this case the normalized difference values.
l7 = ee.ImageCollection('LANDSAT/LE07/C01/T1') \
    .filterDate('2000-01-01', '2001-01-01')
withNd = l7.map(lambda image: image.normalizedDifference(['B4', 'B3']).addBands(image))

# Build a mosaic using the NDVI of bands 4 and 3, essentially showing the
# greenest pixels from the year 2000.
greenest = qualityMosaic(withNd)

# Select out the color bands to visualize. An interesting artifact of this
# approach is that clouds are greener than water. So all the water is white.
rgb = greenest.select(['B3', 'B2', 'B1'])

Map.addLayer(rgb, {'gain': [1.4, 1.4, 1.1]}, 'Greenest')
Map.setCenter(-90.08789, 16.38339, 11)



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map