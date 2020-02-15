'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/ImageCollection/mosaicking.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/ImageCollection/mosaicking.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=ImageCollection/mosaicking.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/ImageCollection/mosaicking.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
</table>
'''

# %%
'''
## Install Earth Engine API
Install the [Earth Engine Python API](https://developers.google.com/earth-engine/python_install) and [geehydro](https://github.com/giswqs/geehydro). The **geehydro** Python package builds on the [folium](https://github.com/python-visualization/folium) package and implements several methods for displaying Earth Engine data layers, such as `Map.addLayer()`, `Map.setCenter()`, `Map.centerObject()`, and `Map.setOptions()`.
The following script checks if the geehydro package has been installed. If not, it will install geehydro, which automatically install its dependencies, including earthengine-api and folium.
'''


# %%
import subprocess

try:
    import geehydro
except ImportError:
    print('geehydro package not installed. Installing ...')
    subprocess.check_call(["python", '-m', 'pip', 'install', 'geehydro'])

# %%
'''
Import libraries
'''


# %%
import ee
import folium
import geehydro

# %%
'''
Authenticate and initialize Earth Engine API. You only need to authenticate the Earth Engine API once. 
'''


# %%
try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize()

# %%
'''
## Create an interactive map 
This step creates an interactive map using [folium](https://github.com/python-visualization/folium). The default basemap is the OpenStreetMap. Additional basemaps can be added using the `Map.setOptions()` function. 
The optional basemaps can be `ROADMAP`, `SATELLITE`, `HYBRID`, `TERRAIN`, or `ESRI`.
'''

# %%
Map = folium.Map(location=[40, -100], zoom_start=4)
Map.setOptions('HYBRID')

# %%
'''
## Add Earth Engine Python script 

'''

# %%
# Load three NAIP quarter quads in the same location, different times.
naip2004_2012 = ee.ImageCollection('USDA/NAIP/DOQQ') \
  .filterBounds(ee.Geometry.Point(-71.08841, 42.39823)) \
  .filterDate('2004-07-01', '2012-12-31') \
  .select(['R', 'G', 'B'])

# Temporally composite the images with a maximum value function.
composite = naip2004_2012.max()
Map.setCenter(-71.12532, 42.3712, 12)
Map.addLayer(composite, {}, 'max value composite')


# Load four 2012 NAIP quarter quads, different locations.
naip2012 = ee.ImageCollection('USDA/NAIP/DOQQ') \
  .filterBounds(ee.Geometry.Rectangle(-71.17965, 42.35125, -71.08824, 42.40584)) \
  .filterDate('2012-01-01', '2012-12-31')

# Spatially mosaic the images in the collection and display.
mosaic = naip2012.mosaic()
Map.setCenter(-71.12532, 42.3712, 12)
Map.addLayer(mosaic, {}, 'spatial mosaic')


# Load a NAIP quarter quad, display.
naip = ee.Image('USDA/NAIP/DOQQ/m_4207148_nw_19_1_20120710')
Map.setCenter(-71.0915, 42.3443, 14)
Map.addLayer(naip, {}, 'NAIP DOQQ')

# Create the NDVI and NDWI spectral indices.
ndvi = naip.normalizedDifference(['N', 'R'])
ndwi = naip.normalizedDifference(['G', 'N'])

# Create some binary images from thresholds on the indices.
# This threshold is designed to detect bare land.
bare1 = ndvi.lt(0.2).And(ndwi.lt(0.3))
# This detects bare land with lower sensitivity. It also detects shadows.
bare2 = ndvi.lt(0.2).And(ndwi.lt(0.8))

# Define visualization parameters for the spectral indices.
ndviViz = {'min': -1, 'max': 1, 'palette': ['FF0000', '00FF00']}
ndwiViz = {'min': 0.5, 'max': 1, 'palette': ['00FFFF', '0000FF']}

# Mask and mosaic visualization images.  The last layer is on top.
mosaic = ee.ImageCollection([
  # NDWI > 0.5 is water.  Visualize it with a blue palette.
  ndwi.updateMask(ndwi.gte(0.5)).visualize(**ndwiViz),
  # NDVI > 0.2 is vegetation.  Visualize it with a green palette.
  ndvi.updateMask(ndvi.gte(0.2)).visualize(**ndviViz),
  # Visualize bare areas with shadow (bare2 but not bare1) as gray.
  bare2.updateMask(bare2.And(bare1.Not())).visualize(**{'palette': ['AAAAAA']}),
  # Visualize the other bare areas as white.
  bare1.updateMask(bare1).visualize(**{'palette': ['FFFFFF']}),
]).mosaic()
Map.addLayer(mosaic, {}, 'Visualization mosaic')



# # This function masks clouds in Landsat 8 imagery.
# maskClouds = function(image) {
#   scored = ee.Algorithms.Landsat.simpleCloudScore(image)
#   return image.updateMask(scored.select(['cloud']).lt(20))
# }

# # This function masks clouds and adds quality bands to Landsat 8 images.
# addQualityBands = function(image) {
#   return maskClouds(image)
#     # NDVI \
#     .addBands(image.normalizedDifference(['B5', 'B4']))
#     # time in days \
#     .addBands(image.metadata('system:time_start'))
# }

# # Load a 2014 Landsat 8 ImageCollection.
# # Map the cloud masking and quality band function over the collection.
# collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
#   .filterDate('2014-06-01', '2014-12-31') \
#   .map(addQualityBands)

# # Create a cloud-free, most recent value composite.
# recentValueComposite = collection.qualityMosaic('system:time_start')

# # Create a greenest pixel composite.
# greenestPixelComposite = collection.qualityMosaic('nd')

# # Display the results.
# Map.setCenter(-122.374, 37.8239, 12) # San Francisco Bay
# vizParams = {'bands': ['B5', 'B4', 'B3'], 'min': 0, 'max': 0.4}
# Map.addLayer(recentValueComposite, vizParams, 'recent value composite')
# Map.addLayer(greenestPixelComposite, vizParams, 'greenest pixel composite')

# # Compare to a cloudy image in the collection.
# cloudy = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140825')
# Map.addLayer(cloudy, vizParams, 'cloudy')



# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map