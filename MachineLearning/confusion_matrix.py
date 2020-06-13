# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/MachineLearning/confusion_matrix.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/MachineLearning/confusion_matrix.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/MachineLearning/confusion_matrix.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Define a region of interest as a point.  Change the coordinates
# to get a classification of any place where there is imagery.
roi = ee.Geometry.Point(-122.3942, 37.7295)

# Load Landsat 5 input imagery.
landsat = ee.Image(ee.ImageCollection('LANDSAT/LT05/C01/T1_TOA')
  # Filter to get only one year of images. \
  .filterDate('2011-01-01', '2011-12-31')
  # Filter to get only images under the region of interest. \
  .filterBounds(roi)
  # Sort by scene cloudiness, ascending. \
  .sort('CLOUD_COVER')
  # Get the first (least cloudy) scene. \
  .first())

# Compute cloud score.
cloudScore = ee.Algorithms.Landsat.simpleCloudScore(landsat).select('cloud')

# Mask the input for clouds.  Compute the min of the input mask to mask
# pixels where any band is masked.  Combine that with the cloud mask.
input = landsat.updateMask(landsat.mask().reduce('min').And(cloudScore.lte(50)))

# Use MODIS land cover, IGBP classification, for training.
modis = ee.Image('MODIS/051/MCD12Q1/2011_01_01') \
    .select('Land_Cover_Type_1')

# Sample the input imagery to get a FeatureCollection of training data.
training = input.addBands(modis).sample(**{
  'numPixels': 5000,
  'seed': 0
})

# Make a Random Forest classifier and train it.
classifier = ee.Classifier.randomForest(10) \
    .train(training, 'Land_Cover_Type_1')

# Classify the input imagery.
classified = input.classify(classifier)

# Get a confusion matrix representing resubstitution accuracy.
trainAccuracy = classifier.confusionMatrix()
print('Resubstitution error matrix: ', trainAccuracy)
print('Training overall accuracy: ', trainAccuracy.accuracy())

# Sample the input with a different random seed to get validation data.
validation = input.addBands(modis).sample(**{
  'numPixels': 5000,
  'seed': 1
  # Filter the result to get rid of any {} pixels.
}).filter(ee.Filter.neq('B1', {}))

# Classify the validation data.
validated = validation.classify(classifier)

# Get a confusion matrix representing expected accuracy.
testAccuracy = validated.errorMatrix('Land_Cover_Type_1', 'classification')
print('Validation error matrix: ', testAccuracy)
print('Validation overall accuracy: ', testAccuracy.accuracy())

# Define a palette for the IGBP classification.
igbpPalette = [
  'aec3d4', # water
  '152106', '225129', '369b47', '30eb5b', '387242', # forest
  '6a2325', 'c3aa69', 'b76031', 'd9903d', '91af40',  # shrub, grass
  '111149', # wetlands
  'cdb33b', # croplands
  'cc0013', # urban
  '33280d', # crop mosaic
  'd7cdcc', # snow and ice
  'f7e084', # barren
  '6f6f6f'  # tundra
]

# Display the input and the classification.
Map.centerObject(ee.FeatureCollection(roi), 10)
Map.addLayer(input, {'bands': ['B3', 'B2', 'B1'], 'max': 0.4}, 'landsat')
Map.addLayer(classified, {'palette': igbpPalette, 'min': 0, 'max': 17}, 'classification')



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map