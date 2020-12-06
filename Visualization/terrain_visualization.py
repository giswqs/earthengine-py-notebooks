# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Visualization/terrain_visualization.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Visualization/terrain_visualization.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Visualization/terrain_visualization.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Use an elevation dataset and terrain functions to create
# a custom visualization of topography.

# Load a global elevation image.
elev = ee.Image('USGS/GMTED2010')

# Zoom to an area of interest.
Map.setCenter(-121.069, 50.709, 6)

# Add the elevation to the map.
Map.addLayer(elev, {}, 'elev')

# Use the terrain algorithms to compute a hillshade with 8-bit values.
shade = ee.Terrain.hillshade(elev)
Map.addLayer(shade, {}, 'hillshade', False)

# Create a "sea" variable to be used for cartographic purposes
sea = elev.lte(0)
Map.addLayer(sea.mask(sea), {'palette':'000022'}, 'sea', False)

# Create a custom elevation palette from hex strings.
elevationPalette = ['006600', '002200', 'fff700', 'ab7634', 'c4d0ff', 'ffffff']
# Use these visualization parameters, customized by location.
visParams = {'min': 1, 'max': 3000, 'palette': elevationPalette}

# Create a mosaic of the sea and the elevation data
visualized = ee.ImageCollection([
  # Mask the elevation to get only land
  elev.mask(sea.Not()).visualize(**visParams),
  # Use the sea mask directly to display sea.
  sea.mask(sea).visualize(**{'palette':'000022'})
]).mosaic()

# Note that the visualization image doesn't require visualization parameters.
Map.addLayer(visualized, {}, 'elev palette', False)

# Convert the visualized elevation to HSV, first converting to [0, 1] data.
hsv = visualized.divide(255).rgbToHsv()
# Select only the hue and saturation bands.
hs = hsv.select(0, 1)
# Convert the hillshade to [0, 1] data, as expected by the HSV algorithm.
v = shade.divide(255)
# Create a visualization image by converting back to RGB from HSV.
# Note the cast to byte in order to export the image correctly.
rgb = hs.addBands(v).hsvToRgb().multiply(255).byte()
Map.addLayer(rgb, {}, 'styled')



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map