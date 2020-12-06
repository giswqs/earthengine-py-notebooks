# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Datasets/Vectors/global_power_plant_database.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Datasets/Vectors/global_power_plant_database.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Datasets/Vectors/global_power_plant_database.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Visualization for WRI/GPPD/power_plants
# https:#code.earthengine.google.com/9efbd726e4a8ba9b8b56ba94f1267678

table = ee.FeatureCollection("WRI/GPPD/power_plants")

# Get a color from a fuel
fuelColor = ee.Dictionary({
  'Coal': '000000',
  'Oil': '593704',
  'Gas': 'BC80BD',
  'Hydro': '0565A6',
  'Nuclear': 'E31A1C',
  'Solar': 'FF7F00',
  'Waste': '6A3D9A',
  'Wind': '5CA2D1',
  'Geothermal': 'FDBF6F',
  'Biomass': '229A00'
})

# List of fuels to add to the map
fuels = ['Coal', 'Oil', 'Gas', 'Hydro', 'Nuclear', 'Solar', 'Waste',
    'Wind', 'Geothermal', 'Biomass']

# /**
#  * Computes size from capacity and color from fuel type.
#  *
#  * @param {!ee.Geometry.Point} pt A point
#  * @return {!ee.Geometry.Point} Input point with added style dictionary.
#  */
def addStyle(pt):
  size = ee.Number(pt.get('capacitymw')).sqrt().divide(10).add(2)
  color = fuelColor.get(pt.get('fuel1'))
  return pt.set('styleProperty', ee.Dictionary({'pointSize': size, 'color': color}))


# Make a FeatureCollection out of the power plant data table
pp = ee.FeatureCollection(table).map(addStyle)
# print(pp.first())

# /**
#  * Adds power plants of a certain fuel type to the map.
#  *
#  * @param {string} fuel A fuel type
#  */
def addLayer(fuel):
#   print(fuel)
  Map.addLayer(pp.filter(ee.Filter.eq('fuel1', fuel)).style({'styleProperty': 'styleProperty', 'neighborhood': 50}), {}, fuel, True, 0.65)


# Apply `addLayer` to each record in `fuels`
for fuel in fuels:
    Map.addLayer(pp.filter(ee.Filter.eq('fuel1', fuel)).style(**{'styleProperty': 'styleProperty', 'neighborhood': 50}), {}, fuel, True, 0.65)


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map