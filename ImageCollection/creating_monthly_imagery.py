# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/ImageCollection/creating_monthly_imagery.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/ImageCollection/creating_monthly_imagery.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/ImageCollection/creating_monthly_imagery.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map