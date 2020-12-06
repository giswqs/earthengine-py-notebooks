# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Image/image_vis.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Image/image_vis.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Image/image_vis.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
image = ee.Image('LANDSAT/LC8_L1T_TOA/LC80440342014077LGN00')
# print(image.getInfo())
Map.setCenter(-122.1899, 37.5010, 10)
vis = {'bands': ['B5', 'B4', 'B3'], 'min': 0, 'max': 0.5, 'gamma': [0.95, 1.1, 1]}
# Map.addLayer(image, vis)


# Color palettes
image = ee.Image('LANDSAT/LC8_L1T_TOA/LC80440342014077LGN00')
ndwi = image.normalizedDifference(['B3', 'B5'])
ndwiViz = {'min': 0.5, 'max': 1, 'palette': ['00FFFF', '0000FF']}
# Map.addLayer(ndwi, ndwiViz, 'NDWI')

# Masking
ndwiMasked = ndwi.updateMask(ndwi.gte(0.4))
# Map.addLayer(ndwiMasked, ndwiViz, 'NDWI masked')

# Create visualization layers.
imageRGB = image.visualize({'bands': ['B5', 'B4', 'B3'], max: 0.5})
ndwiRGB = ndwiMasked.visualize({
    'min': 0.5,
    'max': 1,
    'palette': ['00FFFF', '0000FF']
})

# Mosaic the visualization layers and display( or export).
# mosaic = ee.ImageCollection([imageRGB, ndwiRGB]).mosaic()
# mosaic = ee.ImageCollection([image,ndwiMasked]).mosaic()
# Map.addLayer(mosaic, {}, 'mosaic')


roi = ee.Geometry.Point([-122.4481, 37.7599]).buffer(20000)
Map.addLayer(image.clip(roi), vis, 'Landsat 8')
Map.addLayer(ndwiMasked.clip(roi),ndwiViz, 'NDWI')



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map