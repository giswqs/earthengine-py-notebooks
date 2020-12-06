# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Reducer/stats_of_image_neighborhoods.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Reducer/stats_of_image_neighborhoods.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Reducer/stats_of_image_neighborhoods.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Define a region in the redwood forest.
redwoods = ee.Geometry.Rectangle(-124.0665, 41.0739, -123.934, 41.2029)

# Load input NAIP imagery and build a mosaic.
naipCollection = ee.ImageCollection('USDA/NAIP/DOQQ') \
  .filterBounds(redwoods) \
  .filterDate('2012-01-01', '2012-12-31')
naip = naipCollection.mosaic()

# Compute NDVI from the NAIP imagery.
naipNDVI = naip.normalizedDifference(['N', 'R'])

# Compute standard deviation (SD) as texture of the NDVI.
texture = naipNDVI.reduceNeighborhood(**{
  'reducer': ee.Reducer.stdDev(),
  'kernel': ee.Kernel.circle(7),
})

# Display the results.
Map.centerObject(ee.FeatureCollection(redwoods), 12)
Map.addLayer(naip, {}, 'NAIP input imagery')
Map.addLayer(naipNDVI, {'min': -1, 'max': 1, 'palette': ['FF0000', '00FF00']}, 'NDVI')
Map.addLayer(texture, {'min': 0, 'max': 0.3}, 'SD of NDVI')



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map