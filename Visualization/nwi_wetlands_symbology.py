'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Visualization/nwi_wetlands_symbology.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Visualization/nwi_wetlands_symbology.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Visualization/nwi_wetlands_symbology.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Visualization/nwi_wetlands_symbology.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# NWI legend: https://www.fws.gov/wetlands/Data/Mapper-Wetlands-Legend.html
def nwi_add_color(fc):
    emergent = ee.FeatureCollection(
        fc.filter(ee.Filter.eq('WETLAND_TY', 'Freshwater Emergent Wetland')))
    emergent = emergent.map(lambda f: f.set(
        'R', 127).set('G', 195).set('B', 28))
    # print(emergent.first())

    forested = fc.filter(ee.Filter.eq(
        'WETLAND_TY', 'Freshwater Forested/Shrub Wetland'))
    forested = forested.map(lambda f: f.set('R', 0).set('G', 136).set('B', 55))

    pond = fc.filter(ee.Filter.eq('WETLAND_TY', 'Freshwater Pond'))
    pond = pond.map(lambda f: f.set('R', 104).set('G', 140).set('B', 192))

    lake = fc.filter(ee.Filter.eq('WETLAND_TY', 'Lake'))
    lake = lake.map(lambda f: f.set('R', 19).set('G', 0).set('B', 124))

    riverine = fc.filter(ee.Filter.eq('WETLAND_TY', 'Riverine'))
    riverine = riverine.map(lambda f: f.set(
        'R', 1).set('G', 144).set('B', 191))

    fc = ee.FeatureCollection(emergent.merge(
        forested).merge(pond).merge(lake).merge(riverine))

    base = ee.Image(0).mask(0).toInt8()
    img = base.paint(fc, 'R') \
        .addBands(base.paint(fc, 'G')
                  .addBands(base.paint(fc, 'B')))
    return img


fromFT = ee.FeatureCollection("users/wqs/Pipestem/Pipestem_HUC10")
Map.addLayer(ee.Image().paint(fromFT, 0, 2), {}, 'Watershed')
huc8_id = '10160002'
nwi_asset_path = 'users/wqs/NWI-HU8/HU8_' + huc8_id + '_Wetlands'    # NWI wetlands for the clicked watershed
clicked_nwi_huc = ee.FeatureCollection(nwi_asset_path)
nwi_color = nwi_add_color(clicked_nwi_huc)
Map.centerObject(clicked_nwi_huc, 10)
Map.addLayer(nwi_color, {'gamma': 0.3, 'opacity': 0.7}, 'NWI Wetlands Color')


# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map