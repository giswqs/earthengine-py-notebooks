# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Visualization/visualizing_feature_collection.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Visualization/visualizing_feature_collection.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Visualization/visualizing_feature_collection.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Load a FeatureCollection from a table dataset: 'RESOLVE' ecoregions.
ecoregions = ee.FeatureCollection('RESOLVE/ECOREGIONS/2017')

# Display as default and with a custom color.
Map.addLayer(ecoregions, {}, 'default display')
Map.addLayer(ecoregions, {'color': 'FF0000'}, 'colored')


Map.addLayer(ecoregions.draw(**{'color': '006600', 'strokeWidth': 5}), {}, 'drawn')


# Create an empty image into which to paint the features, cast to byte.
empty = ee.Image().byte()

# Paint all the polygon edges with the same number and 'width', display.
outline = empty.paint(**{
  'featureCollection': ecoregions,
  'color': 1,
  'width': 3
})
Map.addLayer(outline, {'palette': 'FF0000'}, 'edges')


# Paint the edges with different colors, display.
outlines = empty.paint(**{
  'featureCollection': ecoregions,
  'color': 'BIOME_NUM',
  'width': 4
})
palette = ['FF0000', '00FF00', '0000FF']
Map.addLayer(outlines, {'palette': palette, 'max': 14}, 'different color edges')


# Paint the edges with different colors and 'width's.
outlines = empty.paint(**{
  'featureCollection': ecoregions,
  'color': 'BIOME_NUM',
  'width': 'NNH'
})
Map.addLayer(outlines, {'palette': palette, 'max': 14}, 'different color, width edges')


# Paint the interior of the polygons with different colors.
fills = empty.paint(**{
  'featureCollection': ecoregions,
  'color': 'BIOME_NUM',
})
Map.addLayer(fills, {'palette': palette, 'max': 14}, 'colored fills')


# Paint both the fill and the edges.
filledOutlines = empty.paint(ecoregions, 'BIOME_NUM').paint(ecoregions, 0, 2)
Map.addLayer(filledOutlines, {'palette': ['000000'] + palette, 'max': 14}, 'edges and fills')



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map