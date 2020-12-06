# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Array/array_sorting.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Array/array_sorting.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Array/array_sorting.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Define an arbitrary region of interest as a point.
roi = ee.Geometry.Point(-122.26032, 37.87187)

# Use these bands.
bandNames = ee.List(['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'B11'])

# Load a Landsat 8 collection.
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
  .select(bandNames) \
  .filterBounds(roi) \
  .filterDate('2014-06-01', '2014-12-31') \
  .map(lambda image: ee.Algorithms.Landsat.simpleCloudScore(image))

# Convert the collection to an array.
array = collection.toArray()

# Label of the axes.
imageAxis = 0
bandAxis = 1

# Get the cloud slice and the bands of interest.
bands = array.arraySlice(bandAxis, 0, bandNames.length())
clouds = array.arraySlice(bandAxis, bandNames.length())

# Sort by cloudiness.
sorted = bands.arraySort(clouds)

# Get the least cloudy images, 20% of the total.
numImages = sorted.arrayLength(imageAxis).multiply(0.2).int()
leastCloudy = sorted.arraySlice(imageAxis, 0, numImages)

# Get the mean of the least cloudy images by reducing along the image axis.
mean = leastCloudy.arrayReduce(**{
  'reducer': ee.Reducer.mean(),
  'axes': [imageAxis]
})

# Turn the reduced array image into a multi-band image for display.
meanImage = mean.arrayProject([bandAxis]).arrayFlatten([bandNames])
Map.centerObject(ee.FeatureCollection(roi), 12)
Map.addLayer(meanImage, {'bands': ['B5', 'B4', 'B2'], 'min': 0, 'max': 0.5}, 'Mean Image')



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map