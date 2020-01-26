'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/ImageCollection/creating_monthly_imagery.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/ImageCollection/creating_monthly_imagery.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=ImageCollection/creating_monthly_imagery.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/ImageCollection/creating_monthly_imagery.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
p1 = ee.Geometry.Point([103.521, 13.028])
p2 = ee.Geometry.Point([105.622, 13.050])
Date_Start = ee.Date('2000-05-01')
Date_End = ee.Date('2007-12-01')
Date_window = ee.Number(30)

# Create list of dates for time series
n_months = Date_End.difference(Date_Start, 'month').round()
print("Number of months:", n_months.getInfo())
dates = ee.List.sequence(0, n_months, 1)
print(dates.getInfo())

def make_datelist(n):
    return Date_Start.advance(n, 'month')


dates = dates.map(make_datelist)
print(dates.getInfo())


def fnc(d1):
    S1 = ee.ImageCollection('LANDSAT/LT5_L1T_TOA') \
        .filterDate('2000-05-01', '2007-12-01') \
        .filter(ee.Filter.calendarRange(1, 14, 'month')) \
        .sort('CLOUD_COVER') \
        .filterBounds(p1).first()
    S2 = ee.ImageCollection('LANDSAT/LT5_L1T_TOA') \
        .filterDate('2000-05-01', '2007-12-01') \
        .filter(ee.Filter.calendarRange(1, 14, 'month')) \
        .sort('CLOUD_COVER') \
        .filterBounds(p2).first()

    mosaic = ee.ImageCollection([ee.Image(S1), ee.Image(S2)]).mosaic()

    return mosaic


list_of_images = dates.map(fnc)
print('list_of_images', list_of_images.getInfo())
mt = ee.ImageCollection(list_of_images)
print(mt.getInfo())
# Map.addLayer(mt, {}, 'mt')


# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map