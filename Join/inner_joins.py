# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Join/inner_joins.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Join/inner_joins.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Join/inner_joins.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Make a date filter to get images in this date range.
dateFilter = ee.Filter.date('2014-01-01', '2014-02-01')

# Load a MODIS collection with EVI data.
mcd43a4 = ee.ImageCollection('MODIS/MCD43A4_006_EVI') \
    .filter(dateFilter)

# Load a MODIS collection with quality data.
mcd43a2 = ee.ImageCollection('MODIS/006/MCD43A2') \
    .filter(dateFilter)

# Define an inner join.
innerJoin = ee.Join.inner()

# Specify an equals filter for image timestamps.
filterTimeEq = ee.Filter.equals(**{
  'leftField': 'system:time_start',
  'rightField': 'system:time_start'
})

# Apply the join.
innerJoinedMODIS = innerJoin.apply(mcd43a4, mcd43a2, filterTimeEq)

# Display the join result: a FeatureCollection.
print('Inner join output:', innerJoinedMODIS)

# Map a function to merge the results in the output FeatureCollection.
joinedMODIS = innerJoinedMODIS.map(lambda feature: ee.Image.cat(feature.get('primary'), feature.get('secondary')))

# Print the result of merging.
print('Inner join, merged bands:', joinedMODIS.getInfo())



# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map