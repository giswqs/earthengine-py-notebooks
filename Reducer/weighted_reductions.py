# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Reducer/weighted_reductions.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Reducer/weighted_reductions.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Reducer/weighted_reductions.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Load a Landsat 8 input image.
image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318')

# Creat an arbitrary region.
geometry = ee.Geometry.Rectangle(-122.496, 37.532, -121.554, 37.538)

# Make an NDWI image.  It will have one band named 'nd'.
ndwi = image.normalizedDifference(['B3', 'B5'])

# Compute the weighted mean of the NDWI image clipped to the region.
weighted = ndwi.clip(geometry) \
  .reduceRegion(**{
    'reducer': ee.Reducer.sum(),
    'geometry': geometry,
    'scale': 30}) \
  .get('nd')

# Compute the UN-weighted mean of the NDWI image clipped to the region.
unweighted = ndwi.clip(geometry) \
  .reduceRegion(**{
    'reducer': ee.Reducer.sum().unweighted(),
    'geometry': geometry,
    'scale': 30}) \
  .get('nd')

# Observe the difference between weighted and unweighted reductions.
print('weighted:', weighted.getInfo())
print('unweighted', unweighted.getInfo())



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map