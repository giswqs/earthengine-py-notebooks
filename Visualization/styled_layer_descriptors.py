# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Visualization/styled_layer_descriptors.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Visualization/styled_layer_descriptors.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Visualization/styled_layer_descriptors.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
cover = ee.Image('MODIS/051/MCD12Q1/2012_01_01').select('Land_Cover_Type_1')

# Define an SLD style of discrete intervals to apply to the image.
sld_intervals = \
'<RasterSymbolizer>' + \
 ' <ColorMap  type="intervals" extended="false" >' + \
    '<ColorMapEntry color="#aec3d4" quantity="0" label="Water"/>' + \
    '<ColorMapEntry color="#152106" quantity="1" label="Evergreen Needleleaf Forest"/>' + \
    '<ColorMapEntry color="#225129" quantity="2" label="Evergreen Broadleaf Forest"/>' + \
    '<ColorMapEntry color="#369b47" quantity="3" label="Deciduous Needleleaf Forest"/>' + \
    '<ColorMapEntry color="#30eb5b" quantity="4" label="Deciduous Broadleaf Forest"/>' + \
    '<ColorMapEntry color="#387242" quantity="5" label="Mixed Deciduous Forest"/>' + \
    '<ColorMapEntry color="#6a2325" quantity="6" label="Closed Shrubland"/>' + \
    '<ColorMapEntry color="#c3aa69" quantity="7" label="Open Shrubland"/>' + \
    '<ColorMapEntry color="#b76031" quantity="8" label="Woody Savanna"/>' + \
    '<ColorMapEntry color="#d9903d" quantity="9" label="Savanna"/>' + \
    '<ColorMapEntry color="#91af40" quantity="10" label="Grassland"/>' + \
    '<ColorMapEntry color="#111149" quantity="11" label="Permanent Wetland"/>' + \
    '<ColorMapEntry color="#cdb33b" quantity="12" label="Cropland"/>' + \
    '<ColorMapEntry color="#cc0013" quantity="13" label="Urban"/>' + \
    '<ColorMapEntry color="#33280d" quantity="14" label="Crop, Natural Veg. Mosaic"/>' + \
    '<ColorMapEntry color="#d7cdcc" quantity="15" label="Permanent Snow, Ice"/>' + \
    '<ColorMapEntry color="#f7e084" quantity="16" label="Barren, Desert"/>' + \
    '<ColorMapEntry color="#6f6f6f" quantity="17" label="Tundra"/>' + \
  '</ColorMap>' + \
'</RasterSymbolizer>'
Map.addLayer(cover.sldStyle(sld_intervals), {}, 'IGBP classification styled')

# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map