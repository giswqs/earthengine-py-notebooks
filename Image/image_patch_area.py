'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Image/image_patch_area.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Image/image_patch_area.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://mybinder.org/v2/gh/giswqs/earthengine-py-notebooks/master?filepath=Image/image_patch_area.ipynb"><img width=58px src="https://mybinder.org/static/images/logo_social.png" />Run in binder</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Image/image_patch_area.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
geometry = ee.Geometry.Polygon(
        [[[-121.53162002563477, 37.62442917942242],
          [-121.53822898864746, 37.61871860390886],
          [-121.53307914733887, 37.61144378319061],
          [-121.5281867980957, 37.60784010375065],
          [-121.52209281921387, 37.60586820524277],
          [-121.51840209960938, 37.606344185530936],
          [-121.51273727416992, 37.60777210812061],
          [-121.50175094604492, 37.6082480762255],
          [-121.49454116821289, 37.61239566936059],
          [-121.49127960205078, 37.62136999709244],
          [-121.49797439575195, 37.62667249978579],
          [-121.5252685546875, 37.62653654290317]]])

# Load a Landsat 8 image and display the thermal band.
image = ee.Image('LANDSAT/LC8_L1T_TOA/LC80440342014077LGN00').clip(geometry)
Map.setCenter(-121.51385307312012,37.61767615130697, 14) # SF Bay
#Map.addLayer(image, {'bands': ['B10'], 'min': 270, 'max': 310}, 'LST')
#print(image)

# Threshold the thermal band to find "hot" objects.
hotspots = image.select('B10').gt(303)

# Mask "cold" pixels.
hotspots = hotspots.mask(hotspots)
#Map.addLayer(hotspots, {'palette': 'FF0000'}, 'hotspots')

# Compute the number of pixels in each patch.
patchsize = hotspots.connectedPixelCount(100, False)
Map.addLayer(patchsize, {}, 'patch size')
largePatches = patchsize.gt(4)
largePatches = largePatches.updateMask(largePatches)
Map.addLayer(largePatches, {}, 'patch size>4')

pixelAreaAllPatches = hotspots.multiply(ee.Image.pixelArea())
pixelAreaLargePatch = largePatches.multiply(ee.Image.pixelArea())
areaAllPathces = pixelAreaAllPatches.reduceRegion(**{'reducer':ee.Reducer.sum(),'geometry':geometry})
areaLargePatch = pixelAreaLargePatch.reduceRegion(**{'reducer':ee.Reducer.sum(),'geometry':geometry})

print(areaAllPathces.getInfo())
print(areaLargePatch.getInfo())

# %%
'''
## Display Earth Engine data layers 

'''


# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map