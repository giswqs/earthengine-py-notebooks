# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/FeatureCollection/simplify_polygons.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/FeatureCollection/simplify_polygons.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/FeatureCollection/simplify_polygons.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
waterSurface = ee.Image('JRC/GSW1_0/GlobalSurfaceWater')
waterChange = waterSurface.select('transition')
 # Select Permanent Water Only:
Permanent_Water = 1 # value 1 represents pixels of permenant water, no change
waterMask = waterChange.eq(Permanent_Water) # Water mask boolean = 1 to detect whater bodies
# Map.setCenter(24.43874, 61.58173, 10)
# Map.addLayer(waterMask, {}, 'Water Mask')
# Map.centerObject(masked)
OnlyLakes = waterMask.updateMask(waterMask)

roi = ee.Geometry.Polygon(
        [[[22.049560546875, 61.171214253920965],
          [22.0330810546875, 60.833021871926185],
          [22.57415771484375, 60.83168327936567],
          [22.5714111328125, 61.171214253920965]]])

classes = OnlyLakes.reduceToVectors(**{
  'reducer': ee.Reducer.countEvery(),
  'geometry': roi,
  'scale': 30,
  'maxPixels': 1e10
})
simpleClasses = classes.geometry().simplify(50)

Map.centerObject(ee.FeatureCollection(roi), 10)
Map.addLayer(ee.Image().paint(classes, 0, 2),{'palette': 'red'}, "original")
Map.addLayer(ee.Image().paint(simpleClasses, 0, 2),{'palette': 'blue'}, "simplified")


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map