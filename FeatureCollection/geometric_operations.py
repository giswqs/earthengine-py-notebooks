# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/FeatureCollection/geometric_operations.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/FeatureCollection/geometric_operations.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/FeatureCollection/geometric_operations.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Create two circular geometries.
poly1 = ee.Geometry.Point([-50, 30]).buffer(1e6)
poly2 = ee.Geometry.Point([-40, 30]).buffer(1e6)

# Display polygon 1 in red and polygon 2 in blue.
Map.setCenter(-45, 30)
Map.addLayer(poly1, {'color': 'FF0000'}, 'poly1')
Map.addLayer(poly2, {'color': '0000FF'}, 'poly2')

# Compute the intersection, display it in blue.
intersection = poly1.intersection(poly2, ee.ErrorMargin(1))
Map.addLayer(intersection, {'color': '00FF00'}, 'intersection')

# Compute the union, display it in magenta.
union = poly1.union(poly2, ee.ErrorMargin(1))
Map.addLayer(union, {'color': 'FF00FF'}, 'union')

# Compute the difference, display in yellow.
diff1 = poly1.difference(poly2, ee.ErrorMargin(1))
Map.addLayer(diff1, {'color': 'FFFF00'}, 'diff1')

# Compute symmetric difference, display in black.
symDiff = poly1.symmetricDifference(poly2, ee.ErrorMargin(1))
Map.addLayer(symDiff, {'color': '000000'}, 'symmetric difference')



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map