# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Image/object_based.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Image/object_based.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Image/object_based.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# Make an area of interest geometry centered on San Francisco.
point = ee.Geometry.Point(-122.1899, 37.5010)
aoi = point.buffer(10000)

# Import a Landsat 8 image, subset the thermal band, and clip to the
# area of interest.
kelvin = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318') \
  .select(['B10'], ['kelvin']) \
  .clip(aoi)

# Display the thermal band.
# Map.centerObject(point, 13)
Map.setCenter(-122.1899, 37.5010, 13)
Map.addLayer(kelvin, {'min': 288, 'max': 305}, 'Kelvin')


# Threshold the thermal band to set hot pixels as value 1 and not as 0.
hotspots = kelvin.gt(303) \
  .selfMask() \
  .rename('hotspots')

# Display the thermal hotspots on the Map.
Map.addLayer(hotspots, {'palette': 'FF0000'}, 'Hotspots')


# Uniquely label the hotspot image objects.
objectId = hotspots.connectedComponents(**{
  'connectedness': ee.Kernel.plus(1),
  'maxSize': 128
})

# Display the uniquely ID'ed objects to the Map.
Map.addLayer(objectId.randomVisualizer(), {}, 'Objects')


# Compute the number of pixels in each object defined by the "labels" band.
objectSize = objectId.select('labels') \
  .connectedPixelCount(**{
    'maxSize': 128, 'eightConnected': False
  })

# Display object pixel count to the Map.
Map.addLayer(objectSize, {}, 'Object n pixels')


# Get a pixel area image.
pixelArea = ee.Image.pixelArea()

# Multiply pixel area by the number of pixels in an object to calculate
# the object area. The result is an image where each pixel
# of an object relates the area of the object in m^2.
objectArea = objectSize.multiply(pixelArea)

# Display object area to the Map.
Map.addLayer(objectArea, {}, 'Object area m^2')


# Threshold the `objectArea` image to define a mask that will mask out
# objects below a given size (1 hectare in this case).
areaMask = objectArea.gte(10000)

# Update the mask of the `objectId` layer defined previously using the
# minimum area mask just defined.
objectId = objectId.updateMask(areaMask)
Map.addLayer(objectId, {}, 'Large hotspots')


# Make a suitable image for `reduceConnectedComponents()` by adding a label
# band to the `kelvin` temperature image.
kelvin = kelvin.addBands(objectId.select('labels'))

# Calculate the mean temperature per object defined by the previously added
# "labels" band.
patchTemp = kelvin.reduceConnectedComponents(**{
  'reducer': ee.Reducer.mean(),
  'labelBand': 'labels'
})

# Display object mean temperature to the Map.
Map.addLayer(
  patchTemp,
  {'min': 303, 'max': 304, 'palette': ['yellow', 'red']},
  'Mean temperature'
)


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map