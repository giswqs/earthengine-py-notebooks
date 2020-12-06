# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Algorithms/landsat_cloud_score.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Algorithms/landsat_cloud_score.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Algorithms/landsat_cloud_score.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Load a cloudy Landsat scene and display it.
cloudy_scene = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140926')
Map.centerObject(cloudy_scene)
Map.addLayer(cloudy_scene, {'bands': ['B4', 'B3', 'B2'], 'max': 0.4}, 'TOA', False)

# Add a cloud score band.  It is automatically called 'cloud'.
scored = ee.Algorithms.Landsat.simpleCloudScore(cloudy_scene)

# Create a mask from the cloud score and combine it with the image mask.
mask = scored.select(['cloud']).lte(20)

# Apply the mask to the image and display the result.
masked = cloudy_scene.updateMask(mask)
Map.addLayer(masked, {'bands': ['B4', 'B3', 'B2'], 'max': 0.4}, 'masked')

# Load a Landsat 8 composite and set the SENSOR_ID property.
mosaic = ee.Image(ee.ImageCollection('LANDSAT/LC8_L1T_8DAY_TOA').first()) \
  .set('SENSOR_ID', 'OLI_TIRS')

# Cloud score the mosaic and display the result.
scored_mosaic = ee.Algorithms.Landsat.simpleCloudScore(mosaic)
Map.addLayer(scored_mosaic, {'bands': ['B4', 'B3', 'B2'], 'max': 0.4},
    'TOA mosaic', False)





# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map