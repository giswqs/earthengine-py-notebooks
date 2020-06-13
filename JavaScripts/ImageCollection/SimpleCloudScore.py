# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/JavaScripts/ImageCollection/SimpleCloudScore.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/JavaScripts/ImageCollection/SimpleCloudScore.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/JavaScripts/ImageCollection/SimpleCloudScore.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# SimpleCloudScore, an example of computing a cloud-free composite with L8
# by selecting the least-cloudy pixel from the collection.

# A mapping from a common name to the sensor-specific bands.
LC8_BANDS = ['B2',   'B3',    'B4',  'B5',  'B6',    'B7',    'B10']
STD_NAMES = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2', 'temp']

# Compute a cloud score.  This expects the input image to have the common
# band names: ["red", "blue", etc], so it can work across sensors.
def cloudScore(img):
  # A helper to apply an expression and linearly rescale the output.
  def rescale(img, exp, thresholds):
    return img.expression(exp, {'img': img}) \
        .subtract(thresholds[0]).divide(thresholds[1] - thresholds[0])
  

  # Compute several indicators of cloudyness and take the minimum of them.
  score = ee.Image(1.0)
  # Clouds are reasonably bright in the blue band.
  score = score.min(rescale(img, 'img.blue', [0.1, 0.3]))

  # Clouds are reasonably bright in all visible bands.
  score = score.min(rescale(img, 'img.red + img.green + img.blue', [0.2, 0.8]))

  # Clouds are reasonably bright in all infrared bands.
  score = score.min(
      rescale(img, 'img.nir + img.swir1 + img.swir2', [0.3, 0.8]))

  # Clouds are reasonably cool in temperature.
  score = score.min(rescale(img, 'img.temp', [300, 290]))

  # However, clouds are not snow.
  ndsi = img.normalizedDifference(['green', 'swir1'])
  return score.min(rescale(ndsi, 'img', [0.8, 0.6]))


# Filter the TOA collection to a time-range and add the cloudscore band.
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
    .filterDate('2017-05-01', '2017-07-01')

def func_yyl(img):
      # Invert the cloudscore so 1 is least cloudy, and rename the band.
      score = cloudScore(img.select(LC8_BANDS, STD_NAMES))
      score = ee.Image(1).subtract(score).select([0], ['cloudscore'])
      return img.addBands(score) \
    .map(func_yyl)







# Define visualization parameters for a True color image.
vizParams = {'bands': ['B4',  'B3',  'B2'], 'max': 0.4, 'gamma': 1.6}
Map.setCenter(-120.24487, 37.52280, 8)
Map.addLayer(collection.qualityMosaic('cloudscore'), vizParams)


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map