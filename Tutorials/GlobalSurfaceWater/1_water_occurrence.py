# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Tutorials/GlobalSurfaceWater/1_water_occurrence.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Tutorials/GlobalSurfaceWater/1_water_occurrence.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Tutorials/GlobalSurfaceWater/1_water_occurrence.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
###############################
# Asset List
###############################

gsw = ee.Image('JRC/GSW1_1/GlobalSurfaceWater')
occurrence = gsw.select('occurrence')

###############################
# Constants
###############################

VIS_OCCURRENCE = {
  'min':0,
  'max':100,
  'palette': ['red', 'blue']
}
VIS_WATER_MASK = {
  'palette': ['white', 'black']
}

###############################
# Calculations
###############################

# Create a water mask layer, and set the image mask so that non-water areas
# are opaque.
water_mask = occurrence.gt(90).selfMask()

###############################
# Initialize Map Location
###############################

# Uncomment one of the following statements to center the map.
# Map.setCenter(-90.162, 29.8597, 10)   # New Orleans, USA
# Map.setCenter(-114.9774, 31.9254, 10) # Mouth of the Colorado River, Mexico
# Map.setCenter(-111.1871, 37.0963, 11) # Lake Powell, USA
# Map.setCenter(149.412, -35.0789, 11)  # Lake George, Australia
# Map.setCenter(105.26, 11.2134, 9)     # Mekong River Basin, SouthEast Asia
# Map.setCenter(90.6743, 22.7382, 10)   # Meghna River, Bangladesh
# Map.setCenter(81.2714, 16.5079, 11)   # Godavari River Basin Irrigation Project, India
# Map.setCenter(14.7035, 52.0985, 12)   # River Oder, Germany & Poland
# Map.setCenter(-59.1696, -33.8111, 9)  # Buenos Aires, Argentina
Map.setCenter(-74.4557, -8.4289, 11)  # Ucayali River, Peru

###############################
# Map Layers
###############################

Map.addLayer(occurrence.updateMask(occurrence.divide(100)), VIS_OCCURRENCE, "Water Occurrence (1984-2018)")
Map.addLayer(water_mask, VIS_WATER_MASK, '90% occurrence water mask', False)




# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map