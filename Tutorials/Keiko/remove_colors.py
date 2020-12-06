# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Tutorials/Keiko/remove_colors.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Tutorials/Keiko/remove_colors.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Tutorials/Keiko/remove_colors.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Credits to: Keiko Nomura, Senior Analyst, Space Intelligence Ltd
# Source: https://medium.com/google-earth/10-tips-for-becoming-an-earth-engine-expert-b11aad9e598b
# GEE JS: https://code.earthengine.google.com/?scriptPath=users%2Fnkeikon%2Fmedium%3Aremove_colours 

point = ee.Geometry.Point([2.173487088281263, 41.38710609258852])
Map.centerObject(ee.FeatureCollection(point), 11)

# Select the least cloudy image in 2019
image = ee.ImageCollection('COPERNICUS/S2_SR') \
  .filter(ee.Filter.calendarRange(2019, 2019, 'year')) \
  .filterBounds(point) \
  .sort('CLOUDY_PIXEL_PERCENTAGE', True) \
  .select(['B2', 'B3', 'B4', 'B8']) \
  .first()

# print('Image used', image)

Map.addLayer(image, {
  'bands': ['B4', 'B3', 'B2'],
  'min': 0,
  'max': 2500
}, 'RGB (True colours)')
Map.addLayer(image, {
  'bands': ['B3', 'B3', 'B3'],
  'min': 0,
  'max': 2500,
  'gamma': 1.5
}, 'Grey (base)')

# ======= #
#  Green  #
# ======= #

# Select areas with vegetation (higher NDVI)
imageNDVI = image.normalizedDifference(['B8', 'B4']).rename('ndvi')
veg = imageNDVI.gte(0.4)
imageGreen = image.multiply(veg)
imageGreen_vis = imageGreen.selfMask().visualize(**{
  'bands': ['B4', 'B3', 'B2'],
  'min': 0,
  'max': 2500
})
# Increase the strength of colour green to highlight the vegetation
Map.addLayer(imageGreen_vis, {
  'min': [50, 0, 50],
  'max': [255, 200, 255]
}, 'Green', True)

# ======= #
#   Red   #
# ======= #

# Select areas with non-vegetation (lower NDVI) and non-water (NDVI>0)
bare = ee.Image(0).where(imageNDVI.gt(0), 1).where(imageNDVI.gt(0.1), 0)
imageRed = image.multiply(bare)
imageRed_vis = imageRed.selfMask().visualize(**{
  'bands': ['B4', 'B3', 'B2'],
  'min': 0,
  'max': 2500
})
# Increase the strength of colour red
Map.addLayer(imageRed_vis, {
  'min': [0, 50, 50],
  'max': [255, 255, 255]
}, 'Red', False)

# ======== #
#   Blue   #
# ======== #

# Select areas with higher Normalised Difference Water Index (NDWI)
# You can also use nir band (use Otsu method to find a threshold)
imageNDWI = image.normalizedDifference(['B3', 'B8']).rename('ndwi')
water = imageNDWI.gte(0.2)
imageBlue = image.multiply(water)
imageBlue_vis = imageBlue.selfMask().visualize(**{
  'bands': ['B4', 'B3', 'B2'],
  'min': 0,
  'max': 2500
})
# Increase the strength of colour blue to highlight the water
Map.addLayer(imageBlue_vis, {
  'min': [10, 10, 0],
  'max': [255, 255, 200]
}, 'Blue', False)

# ======== #
#  Export  #
# ======== #

# Export the image as a mosaic (e.g. green), or use blend()
grey = image.multiply(veg.select('ndvi').lt(0.4))
mosaicGreen = ee.ImageCollection([
  imageGreen_vis.visualize(**{
    'min': [50, 0, 50],
    'max': [255, 200, 255]
  }),
  grey.selfMask().visualize(**{
    'bands': ['B3', 'B3', 'B3'],
    'min': 0,
    'max': 2500,
    'gamma': 1.5
  }),
]).mosaic()
#Map.addLayer(mosaicGreen, {}, 'export')

# Export.image.toDrive({
#   'image': mosaicGreen,
#   description: 'green',
#   'region': point.buffer(10000).bounds(),
#   crs: 'EPSG:3857',
#   'scale': 10
# })

# Other examples
population = ee.Image("WorldPop/GP/100m/pop/ESP_2019")
pop_vis = {
  'min': 0.0,
  'max': 200.0,
  'opacity': 0.3,
  'palette': ['0000C0', 'FFFF80', 'C00000'],
}
Map.addLayer(population, pop_vis, 'Population', False)

collectionCO = ee.ImageCollection('COPERNICUS/S5P/NRTI/L3_CO') \
  .select('CO_column_number_density') \
  .filterDate('2019-01-01', '2019-12-31')

CO_viz = {
  'min': 0.031,
  'max': 0.034,
  'opacity': 0.3,
  'palette': ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']
}

Map.addLayer(collectionCO.mean(), CO_viz, 'Carbon Monoxide', False)

# ============ #
#  Topography  #
# ============ #

# Optional: add topography by computing a hillshade using the terrain algorithms
elev = ee.Image('USGS/SRTMGL1_003')
shade = ee.Terrain.hillshade(elev)

greenTR = ee.ImageCollection([
  imageGreen_vis.visualize(**{
    'min': [50, 0, 50],
    'max': [255, 200, 255]
  }),
  shade.visualize(**{
    'bands': ['hillshade', 'hillshade', 'hillshade'],
    'opacity': 0.3
  }),
]).mosaic()

Map.addLayer(greenTR.mask(imageGreen_vis), {
}, 'Green (with topography)', False)

# Convert the visualized elevation to HSV, first converting to [0, 1] data.
hsv = greenTR.divide(255).rgbToHsv()
# Select only the hue and saturation bands.
hs = hsv.select(0, 1)
# Convert the hillshade to [0, 1] data, as expected by the HSV algorithm.
v = shade.divide(255)
# Create a visualization image by converting back to RGB from HSV.
# Note the cast to byte in order to export the image correctly.
rgb = hs.addBands(v).hsvToRgb().multiply(255).byte()
Map.addLayer(rgb.mask(imageGreen_vis), {'gamma': 0.6}, 'Green (topography visualised)', False)

# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map