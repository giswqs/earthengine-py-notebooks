# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/NAIP/metadata.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/NAIP/metadata.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/NAIP/metadata.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map