# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/FeatureCollection/from_polygons.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/FeatureCollection/from_polygons.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/FeatureCollection/from_polygons.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
Map.setCenter(-107, 41, 6)

fc = ee.FeatureCollection([
    ee.Feature(
        ee.Geometry.Polygon(
            [[-109.05, 41], [-109.05, 37], [-102.05, 37], [-102.05, 41]]),
        {'name': 'Colorado', 'fill': 1}),
    ee.Feature(
        ee.Geometry.Polygon(
            [[-114.05, 37.0], [-109.05, 37.0], [-109.05, 41.0],
             [-111.05, 41.0], [-111.05, 42.0], [-114.05, 42.0]]),
        {'name': 'Utah', 'fill': 2})
    ])

# Fill, then outline the polygons into a blank image.
image1 = ee.Image(0).mask(0).toByte()
image2 = image1.paint(fc, 'fill')  # Get color from property named 'fill'
image3 = image2.paint(fc, 3, 5)    # Outline using color 3, width 5.

Map.addLayer(image3, {
    'palette': ['000000', 'FF0000', '00FF00', '0000FF'],
    'max': 3,
    'opacity': 0.5
}, "Colorado & Utah")


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map