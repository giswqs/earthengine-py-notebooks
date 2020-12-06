# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Datasets/Vectors/us_census_datasets.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Datasets/Vectors/us_census_datasets.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Datasets/Vectors/us_census_datasets.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
dataset = ee.FeatureCollection('TIGER/2010/Blocks')
visParams = {
  'min': 0.0,
  'max': 700.0,
  'palette': ['black', 'brown', 'yellow', 'orange', 'red']
}

# Turn the strings into numbers
dataset = dataset.map(lambda f: f.set('pop10', ee.Number.parse(f.get('pop10'))))

image = ee.Image().float().paint(dataset, 'pop10')

Map.setCenter(-73.99172, 40.74101, 13)
Map.addLayer(image, visParams, 'TIGER/2010/Blocks')
# Map.addLayer(dataset, {}, 'for Inspector', False)


dataset = ee.FeatureCollection('TIGER/2010/Tracts_DP1')
visParams = {
  'min': 0,
  'max': 4000,
  'opacity': 0.8,
}

# Turn the strings into numbers
dataset = dataset.map(lambda f: f.set('shape_area', ee.Number.parse(f.get('dp0010001'))))

# Map.setCenter(-103.882, 43.036, 8)
image = ee.Image().float().paint(dataset, 'dp0010001')

Map.addLayer(image, visParams, 'TIGER/2010/Tracts_DP1')
# Map.addLayer(dataset, {}, 'for Inspector', False)


dataset = ee.FeatureCollection('TIGER/2010/ZCTA5')
visParams = {
  'palette': ['black', 'purple', 'blue', 'green', 'yellow', 'orange', 'red'],
  'min': 500000,
  'max': 1000000000,
}

zctaOutlines = ee.Image().float().paint(**{
  'featureCollection': dataset,
  'color': 'black',
  'width': 1
})

image = ee.Image().float().paint(dataset, 'ALAND10')
# Map.setCenter(-93.8008, 40.7177, 6)
Map.addLayer(image, visParams, 'TIGER/2010/ZCTA5')
Map.addLayer(zctaOutlines, {}, 'borders')
# Map.addLayer(dataset, {}, 'for Inspector', False)


dataset = ee.FeatureCollection('TIGER/2016/Roads')
roads = dataset.style(**{'color': '#4285F4', 'width': 1})
Map.setCenter(-73.99172, 40.74101, 12)
Map.addLayer(roads, {}, 'TIGER/2016/Roads')


dataset = ee.FeatureCollection('TIGER/2018/Counties')
visParams = {
  'palette': ['purple', 'blue', 'green', 'yellow', 'orange', 'red'],
  'min': 0,
  'max': 50,
  'opacity': 0.8,
}

# Turn the strings into numbers
dataset = dataset.map(lambda f: f.set('STATEFP', ee.Number.parse(f.get('STATEFP'))))

image = ee.Image().float().paint(dataset, 'STATEFP')
countyOutlines = ee.Image().float().paint(**{
  'featureCollection': dataset,
  'color': 'black',
  'width': 1
})

# Map.setCenter(-99.844, 37.649, 5)
Map.addLayer(image, visParams, 'TIGER/2018/Counties')
Map.addLayer(countyOutlines, {}, 'county outlines')
# Map.addLayer(dataset, {}, 'for Inspector', False)


dataset = ee.FeatureCollection('TIGER/2018/States')
visParams = {
  'palette': ['purple', 'blue', 'green', 'yellow', 'orange', 'red'],
  'min': 500000000.0,
  'max': 5e+11,
  'opacity': 0.8,
}
image = ee.Image().float().paint(dataset, 'ALAND')
# Map.setCenter(-99.844, 37.649, 5)
Map.addLayer(image, visParams, 'TIGER/2018/States')
# Map.addLayer(dataset, {}, 'for Inspector', False)


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map