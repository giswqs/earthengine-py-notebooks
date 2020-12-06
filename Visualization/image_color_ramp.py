# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Visualization/image_color_ramp.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Visualization/image_color_ramp.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Visualization/image_color_ramp.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Load SRTM Digital Elevation Model data.
image = ee.Image('CGIAR/SRTM90_V4');

# Define an SLD style of discrete intervals to apply to the image.
sld_intervals = \
  '<RasterSymbolizer>' + \
    '<ColorMap  type="intervals" extended="false" >' + \
      '<ColorMapEntry color="#0000ff" quantity="0" label="0"/>' + \
      '<ColorMapEntry color="#00ff00" quantity="100" label="1-100" />' + \
      '<ColorMapEntry color="#007f30" quantity="200" label="110-200" />' + \
      '<ColorMapEntry color="#30b855" quantity="300" label="210-300" />' + \
      '<ColorMapEntry color="#ff0000" quantity="400" label="310-400" />' + \
      '<ColorMapEntry color="#ffff00" quantity="1000" label="410-1000" />' + \
    '</ColorMap>' + \
  '</RasterSymbolizer>';

# Define an sld style color ramp to apply to the image.
sld_ramp = \
  '<RasterSymbolizer>' + \
    '<ColorMap type="ramp" extended="false" >' + \
      '<ColorMapEntry color="#0000ff" quantity="0" label="0"/>' + \
      '<ColorMapEntry color="#00ff00" quantity="100" label="100" />' + \
      '<ColorMapEntry color="#007f30" quantity="200" label="200" />' + \
      '<ColorMapEntry color="#30b855" quantity="300" label="300" />' + \
      '<ColorMapEntry color="#ff0000" quantity="400" label="400" />' + \
      '<ColorMapEntry color="#ffff00" quantity="500" label="500" />' + \
    '</ColorMap>' + \
  '</RasterSymbolizer>';

# Add the image to the map using both the color ramp and interval schemes.
Map.setCenter(-76.8054, 42.0289, 8);
Map.addLayer(image.sldStyle(sld_intervals), {}, 'SLD intervals');
Map.addLayer(image.sldStyle(sld_ramp), {}, 'SLD ramp');

# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map