# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/JavaScripts/Demos/EgyptClassification.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/JavaScripts/Demos/EgyptClassification.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/JavaScripts/Demos/EgyptClassification.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Upsample MODIS landcover classification (250m) to Landsat
# resolution (30m) using a supervised classifier.

geometry = ee.Geometry.Polygon(
        [[[29.972731783841393, 31.609824974226175],
          [29.972731783841393, 30.110383818311096],
          [32.56550522134139, 30.110383818311096],
          [32.56550522134139, 31.609824974226175]]], {}, False)

# Use the MCD12 land-cover as training data.
collection = ee.ImageCollection('MODIS/006/MCD12Q1')
# See the collection docs to get details on classification system.
modisLandcover = collection \
    .filterDate('2001-01-01', '2001-12-31') \
    .first() \
    .select('LC_Type1') \
    .subtract(1)

# A pallete to use for visualizing landcover images.  You can get this
# from the properties of the collection.
landcoverPalette = '05450a,086a10,54a708,78d203,009900,c6b044,dcd159,' + \
    'dade48,fbff13,b6ff05,27ff87,c24f44,a5a5a5,ff6d4c,69fff8,f9ffa4,1c0dff'
# A set of visualization parameters using the landcover palette.
landcoverVisualization = {'palette': landcoverPalette, 'min': 0, 'max': 16, 'format': 'png'}
# Center over our region of interest.
Map.centerObject(geometry, 11)
# Draw the MODIS landcover image.
Map.addLayer(modisLandcover, landcoverVisualization, 'MODIS landcover')

# Load and filter Landsat data.
l7 = ee.ImageCollection('LANDSAT/LE07/C01/T1') \
    .filterBounds(geometry) \
    .filterDate('2000-01-01', '2001-01-01')

# Draw the Landsat composite, visualizing True color bands.
landsatComposite = ee.Algorithms.Landsat.simpleComposite({
  'collection': l7,
  'asFloat': True
})
Map.addLayer(landsatComposite, {'min': 0, 'max': 0.3, 'bands': ['B3','B2','B1']}, 'Landsat composite')

# Make a training dataset by sampling the stacked images.
training = modisLandcover.addBands(landsatComposite).sample({
  'region': geometry,
  'scale': 30,
  'numPixels': 1000
})

# Train a classifier using the training data.
classifier = ee.Classifier.smileCart().train({
  'features': training,
  'classProperty': 'LC_Type1',
})

# Apply the classifier to the original composite.
upsampled = landsatComposite.classify(classifier)

# Draw the upsampled landcover image.
Map.addLayer(upsampled, landcoverVisualization, 'Upsampled landcover')

# Show the training area.
Map.addLayer(geometry, {}, 'Training region', False)


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map