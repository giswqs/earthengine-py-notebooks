'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/NAIP/metadata.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/NAIP/metadata.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=NAIP/metadata.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/NAIP/metadata.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
</table>
'''

# %%
'''
## Install Earth Engine API
Install the [Earth Engine Python API](https://developers.google.com/earth-engine/python_install) and [geehydro](https://github.com/giswqs/geehydro). The **geehydro** Python package builds on the [folium](https://github.com/python-visualization/folium) package and implements several methods for displaying Earth Engine data layers, such as `Map.addLayer()`, `Map.setCenter()`, `Map.centerObject()`, and `Map.setOptions()`.
The magic command `%%capture` can be used to hide output from a specific cell.
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
if you are running this notebook for this first time or if you are getting an authentication error.  
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
# fc = (ee.FeatureCollection('ft:1fRY18cjsHzDgGiJiS2nnpUU3v9JPDc2HNaR7Xk8')
#       .filter(ee.Filter().eq('Name', 'Minnesota')))

def print_image_id(image):
    index = image.get('system:time_start')
    print(index.getInfo())


lat = 46.80514
lng = -99.22023
lng_lat = ee.Geometry.Point(lng, lat)

collection = ee.ImageCollection('USDA/NAIP/DOQQ')
naip = collection.filterBounds(lng_lat)
naip_2015 = naip.filterDate('2010-01-01', '2015-12-31')

# print(naip_2015.getInfo())
# print(naip_2015.map(print_image_id))
# Map.setCenter(lon, lat, 13)
# Map.addLayer(naip_2015)


image = ee.Image('USDA/NAIP/DOQQ/m_4609915_sw_14_1_20100629')
bandNames = image.bandNames()
print('Band names: ', bandNames.getInfo())

b_nir = image.select('N')

proj = b_nir.projection()
print('Projection: ', proj.getInfo())

props = b_nir.propertyNames()
print(props.getInfo())

img_date = ee.Date(image.get('system:time_start'))
print('Timestamp: ', img_date.getInfo())

id = image.get('system:index')
print(id.getInfo())

# print(image.getInfo())

vis = {'bands': ['N', 'R', 'G']}
# Map.setCenter(lng, lat, 12)
# Map.addLayer(image,vis)


size = naip_2015.toList(100).length()
print("Number of images: ", size.getInfo())

count = naip_2015.size()
print("Count: ", count.getInfo())

dates = ee.List(naip_2015.get('date_range'))
date_range = ee.DateRange(dates.get(0),dates.get(1))
print("Date range: ", date_range.getInfo())


# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map