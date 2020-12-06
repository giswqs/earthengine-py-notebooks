# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/GetStarted/04_band_math.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/GetStarted/04_band_math.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/GetStarted/04_band_math.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# This function gets NDVI from Landsat 5 imagery.


def getNDVI(image):
    return image.normalizedDifference(['B4', 'B3'])


# Load two Landsat 5 images, 20 years apart.
image1 = ee.Image('LANDSAT/LT05/C01/T1_TOA/LT05_044034_19900604')
image2 = ee.Image('LANDSAT/LT05/C01/T1_TOA/LT05_044034_20100611')

# Compute NDVI from the scenes.
ndvi1 = getNDVI(image1)
ndvi2 = getNDVI(image2)

# Compute the difference in NDVI.
ndviDifference = ndvi2.subtract(ndvi1)

ndviParams = {'palette': ['#d73027', '#f46d43', '#fdae61',
                          '#fee08b', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850']}
ndwiParams = {'min': -0.5, 'max': 0.5, 'palette': ['FF0000', 'FFFFFF', '0000FF']}


Map.centerObject(image1, 10)
Map.addLayer(ndvi1, ndviParams, 'NDVI 1')
Map.addLayer(ndvi2, ndviParams, 'NDVI 2')
Map.addLayer(ndviDifference, ndwiParams, 'NDVI difference')


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map