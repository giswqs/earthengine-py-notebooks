# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Join/intersect.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Join/intersect.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Join/intersect.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
def intersect(state):
  nPowerPlants = ee.List(state.get('power_plants')).size()
  # Return the state feature with a new property: power plant count.
  return state.set('n_power_plants', nPowerPlants)

# Load the primary 'collection': US state boundaries.
states = ee.FeatureCollection('TIGER/2018/States')

# Load the secondary 'collection': power plants.
powerPlants = ee.FeatureCollection('WRI/GPPD/power_plants')

# Define a spatial filter as geometries that intersect.
spatialFilter = ee.Filter.intersects(**{
  'leftField': '.geo',
  'rightField': '.geo',
  'maxError': 10
})

# Define a save all join.
saveAllJoin = ee.Join.saveAll(**{
  'matchesKey': 'power_plants',
})

# Apply the join.
intersectJoined = saveAllJoin.apply(states, powerPlants, spatialFilter)

# Add power plant count per state as a property.
intersectJoined = intersectJoined.map(intersect)
# intersectJoined = intersectJoined.map(function(state) {
#   # Get "power_plant" intersection list, count how many intersected this state.
#   nPowerPlants = ee.List(state.get('power_plants')).size()
#   # Return the state feature with a new property: power plant count.
#   return state.set('n_power_plants', nPowerPlants)
# })

print(intersectJoined.getInfo())

# # Make a bar chart for the number of power plants per state.
# chart = ui.Chart.feature.byFeature(intersectJoined, 'NAME', 'n_power_plants') \
#   .setChartType('ColumnChart') \
#   .setSeriesNames({n_power_plants: 'Power plants'}) \
#   .setOptions({
#     title: 'Power plants per state',
#     hAxis: {title: 'State'},
#     vAxis: {title: 'Frequency'}})

# # Print the chart to the console.
# print(chart)


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map