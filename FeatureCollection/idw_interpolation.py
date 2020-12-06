# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/FeatureCollection/idw_interpolation.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/FeatureCollection/idw_interpolation.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/FeatureCollection/idw_interpolation.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
def sampling(sample):
    lat = sample.get('latitude')
    lon = sample.get('longitude')
    ch4 = sample.get('ch4')
    return ee.Feature(ee.Geometry.Point([lon, lat]), {'ch4': ch4})

# Import two weeks of S5P methane and composite by mean.
ch4 = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_CH4') \
  .select('CH4_column_volume_mixing_ratio_dry_air') \
  .filterDate('2019-08-01', '2019-08-15') \
  .mean() \
  .rename('ch4')

# Define an area to perform interpolation over.
aoi = ee.Geometry.Polygon(
    [[[-95.68487605978851, 43.09844605027055],
       [-95.68487605978851, 37.39358590079781],
       [-87.96148738791351, 37.39358590079781],
       [-87.96148738791351, 43.09844605027055]]], {}, False)

# Sample the methane composite to generate a FeatureCollection.
samples = ch4.addBands(ee.Image.pixelLonLat()) \
  .sample(**{'region': aoi, 'numPixels': 1500,
    'scale':1000, 'projection': 'EPSG:4326'}) \
  .map(sampling)

# Combine mean and standard deviation reducers for efficiency.
combinedReducer = ee.Reducer.mean().combine(**{
  'reducer2': ee.Reducer.stdDev(),
  'sharedInputs': True})

# Estimate global mean and standard deviation from the points.
stats = samples.reduceColumns(**{
  'reducer': combinedReducer,
  'selectors': ['ch4']})

# Do the interpolation, valid to 70 kilometers.
interpolated = samples.inverseDistance(**{
  'range': 7e4,
  'propertyName': 'ch4',
  'mean': stats.get('mean'),
  'stdDev': stats.get('stdDev'),
  'gamma': 0.3})

# Define visualization arguments.
band_viz = {
  'min': 1800,
  'max': 1900,
  'palette': ['0D0887', '5B02A3', '9A179B', 'CB4678',
            'EB7852', 'FBB32F', 'F0F921']}

# Display to map.
# Map.centerObject(ee.FeatureCollection(aoi), 7)
Map.addLayer(ch4, band_viz, 'CH4')
# Map.addLayer(interpolated, band_viz, 'CH4 Interpolated')


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map