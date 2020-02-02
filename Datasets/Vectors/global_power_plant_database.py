'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Datasets/Vectors/global_power_plant_database.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Datasets/Vectors/global_power_plant_database.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Datasets/Vectors/global_power_plant_database.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Datasets/Vectors/global_power_plant_database.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
</table>
'''

# %%
'''
## Install Earth Engine API
Install the [Earth Engine Python API](https://developers.google.com/earth-engine/python_install) and [geehydro](https://github.com/giswqs/geehydro). The **geehydro** Python package builds on the [folium](https://github.com/python-visualization/folium) package and implements several methods for displaying Earth Engine data layers, such as `Map.addLayer()`, `Map.setCenter()`, `Map.centerObject()`, and `Map.setOptions()`.
The magic command `%%capture` can be used to hide output from a specific cell. Uncomment these lines if you are running this notebook for the first time.
'''


# %%
# %%capture
# !pip install earthengine-api
# !pip install geehydro

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
Authenticate and initialize Earth Engine API. You only need to authenticate the Earth Engine API once. Uncomment the line `ee.Authenticate()` 
if you are running this notebook for the first time or if you are getting an authentication error.  
'''


# %%
# ee.Authenticate()
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
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map