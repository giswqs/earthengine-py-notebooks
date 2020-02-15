'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Visualization/image_color_ramp.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Visualization/image_color_ramp.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Visualization/image_color_ramp.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Visualization/image_color_ramp.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
</table>
'''

# %%
'''
## Install Earth Engine API
Install the [Earth Engine Python API](https://developers.google.com/earth-engine/python_install) and [geehydro](https://github.com/giswqs/geehydro). The **geehydro** Python package builds on the [folium](https://github.com/python-visualization/folium) package and implements several methods for displaying Earth Engine data layers, such as `Map.addLayer()`, `Map.setCenter()`, `Map.centerObject()`, and `Map.setOptions()`.
The following script checks if the geehydro package has been installed. If not, it will install geehydro, which automatically install its dependencies, including earthengine-api and folium.
'''


# %%
import subprocess

try:
    import geehydro
except ImportError:
    print('geehydro package not installed. Installing ...')
    subprocess.check_call(["python", '-m', 'pip', 'install', 'geehydro'])

# %%
'''
Import libraries
'''


# %%
import ee
import folium
import geehydro

# %%
'''
Authenticate and initialize Earth Engine API. You only need to authenticate the Earth Engine API once. 
'''


# %%
try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize()

# %%
'''
## Create an interactive map 
This step creates an interactive map using [folium](https://github.com/python-visualization/folium). The default basemap is the OpenStreetMap. Additional basemaps can be added using the `Map.setOptions()` function. 
The optional basemaps can be `ROADMAP`, `SATELLITE`, `HYBRID`, `TERRAIN`, or `ESRI`.
'''

# %%
Map = folium.Map(location=[40, -100], zoom_start=4)
Map.setOptions('HYBRID')

# %%
'''
## Add Earth Engine Python script 

'''

# %%
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
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map