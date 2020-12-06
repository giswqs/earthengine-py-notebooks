# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Reducer/convert_raster_to_vector.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Reducer/convert_raster_to_vector.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Reducer/convert_raster_to_vector.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Load a Japan boundary from the Large Scale International Boundary dataset.
japan = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017') \
  .filter(ee.Filter.eq('country_na', 'Japan'))

# Load a 2012 nightlights image, clipped to the Japan border.
nl2012 = ee.Image('NOAA/DMSP-OLS/NIGHTTIME_LIGHTS/F182012') \
  .select('stable_lights') \
  .clipToCollection(japan)

# Define arbitrary thresholds on the 6-bit nightlights image.
zones = nl2012.gt(30).add(nl2012.gt(55)).add(nl2012.gt(62))
zones = zones.updateMask(zones.neq(0))

# Convert the zones of the thresholded nightlights to vectors.
vectors = zones.addBands(nl2012).reduceToVectors(**{
  'geometry': japan,
  'crs': nl2012.projection(),
  'scale': 1000,
  'geometryType': 'polygon',
  'eightConnected': False,
  'labelProperty': 'zone',
  'reducer': ee.Reducer.mean()
})

# Display the thresholds.
Map.setCenter(139.6225, 35.712, 9)
Map.addLayer(zones, {'min': 1, 'max': 3, 'palette': ['0000FF', '00FF00', 'FF0000']}, 'raster')

# Make a display image for the vectors, add it to the map.
display = ee.Image(0).updateMask(0).paint(vectors, '000000', 3)
Map.addLayer(display, {'palette': '000000'}, 'vectors')



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map