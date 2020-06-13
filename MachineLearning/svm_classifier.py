# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/MachineLearning/svm_classifier.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/MachineLearning/svm_classifier.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/MachineLearning/svm_classifier.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Input imagery is a cloud-free Landsat 8 composite.
l8 = ee.ImageCollection('LANDSAT/LC08/C01/T1')

image = ee.Algorithms.Landsat.simpleComposite(**{
  'collection': l8.filterDate('2018-01-01', '2018-12-31'),
  'asFloat': True
})

# Use these bands for prediction.
bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'B11']

# Manually created polygons.
forest1 = ee.Geometry.Rectangle(-63.0187, -9.3958, -62.9793, -9.3443)
forest2 = ee.Geometry.Rectangle(-62.8145, -9.206, -62.7688, -9.1735)
nonForest1 = ee.Geometry.Rectangle(-62.8161, -9.5001, -62.7921, -9.4486)
nonForest2 = ee.Geometry.Rectangle(-62.6788, -9.044, -62.6459, -8.9986)

# Make a FeatureCollection from the hand-made geometries.
polygons = ee.FeatureCollection([
  ee.Feature(nonForest1, {'class': 0}),
  ee.Feature(nonForest2, {'class': 0}),
  ee.Feature(forest1, {'class': 1}),
  ee.Feature(forest2, {'class': 1}),
])

# Get the values for all pixels in each polygon in the training.
training = image.sampleRegions(**{
  # Get the sample from the polygons FeatureCollection.
  'collection': polygons,
  # Keep this list of properties from the polygons.
  'properties': ['class'],
  # Set the scale to get Landsat pixels in the polygons.
  'scale': 30
})

# Create an SVM classifier with custom parameters.
classifier = ee.Classifier.svm(**{
  'kernelType': 'RBF',
  'gamma': 0.5,
  'cost': 10
})

# Train the classifier.
trained = classifier.train(training, 'class', bands)

# Classify the image.
classified = image.classify(trained)

# Display the classification result and the input image.
Map.setCenter(-62.836, -9.2399, 9)
Map.addLayer(image, {'bands': ['B4', 'B3', 'B2'], 'max': 0.5, 'gamma': 2})
Map.addLayer(polygons, {}, 'training polygons')
Map.addLayer(classified,
             {'min': 0, 'max': 1, 'palette': ['red', 'green']},
             'deforestation')



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map