# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/ImageCollection/expression_map.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/ImageCollection/expression_map.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/ImageCollection/expression_map.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
fc = ee.FeatureCollection('TIGER/2018/States').filter(ee.Filter.eq('STUSPS', 'MN'))
# Filter the L7 collection to a single month.
collection = (ee.ImageCollection('LE7_L1T_TOA')
              .filterDate("2002-11-01", "2002-12-01")
              .filterBounds(fc))

def NDVI(image):
  """A function to compute NDVI."""
  return image.expression('float(b("B4") - b("B3")) / (b("B4") + b("B3"))')


def SAVI(image):
  """A function to compute Soil Adjusted Vegetation Index."""
  return ee.Image(0).expression(
      '(1 + L) * float(nir - red)/ (nir + red + L)',
      {
          'nir': image.select('B4'),
          'red': image.select('B3'),
          'L': 0.2
      })

vis = {
    'min': 0,
    'max': 1,
    'palette': [
        'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163',
        '99B718', '74A901', '66A000', '529400', '3E8601',
        '207401', '056201', '004C00', '023B01', '012E01',
        '011D01', '011301'
    ]}

Map.setCenter(-110, 40, 5)
Map.addLayer(collection.map(NDVI).mean(), vis)
Map.addLayer(collection.map(SAVI).mean(), vis)



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map