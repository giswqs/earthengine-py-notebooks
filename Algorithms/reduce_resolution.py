# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Algorithms/reduce_resolution.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Algorithms/reduce_resolution.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Algorithms/reduce_resolution.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Load a MODIS EVI image.
modis = ee.Image(ee.ImageCollection('MODIS/006/MOD13A1').first()) \
    .select('EVI')

# Display the EVI image near La Honda, California.
Map.setCenter(-122.3616, 37.5331, 12)
Map.addLayer(modis, {'min': 2000, 'max': 5000}, 'MODIS EVI')

# Get information about the MODIS projection.
modisProjection = modis.projection()
print('MODIS projection:', modisProjection.getInfo())

# Load and display forest cover data at 30 meters resolution.
forest = ee.Image('UMD/hansen/global_forest_change_2015') \
    .select('treecover2000')
Map.addLayer(forest, {'max': 80}, 'forest cover 30 m')

# Get the forest cover data at MODIS scale and projection.
forestMean = forest \
    .reduceResolution(**{
      'reducer': ee.Reducer.mean(),
      'maxPixels': 1024
    }) \
    .reproject(**{
      'crs': modisProjection
    })

# Display the aggregated, reprojected forest cover data.
Map.addLayer(forestMean, {'max': 80}, 'forest cover at MODIS scale')


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map