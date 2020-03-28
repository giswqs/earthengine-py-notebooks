# %%
'''
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Image/image_visualization.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Image/image_visualization.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Image/image_visualization.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
</table>
'''

# %%
'''
## Image Visualization

This notebook was adapted from the [Earth Engine JavaScript API Documentation](https://developers.google.com/earth-engine/image_visualization). 

The [Get Started](https://developers.google.com/earth-engine/getstarted#adding-data-to-the-map) page illustrates how to visualize an image using `Map.addLayer()`. If you add a layer to the map without any additional parameters, by default the Code Editor assigns the first three bands to red, green and blue, respectively. The default stretch is based on the type of data in the band (e.g. floats are stretched in `[0,1]`, 16-bit data are stretched to the full range of possible values), which may or may not be suitable. To achieve desirable visualization effects, you can provide visualization parameters to `Map.addLayer()`. 

![](https://i.imgur.com/xpWpOal.png)
'''

# %%
'''
## Install and import libraries
'''

# %%
import subprocess

try:
    import geehydro
except ImportError:
    print('geehydro package not installed. Installing ...')
    subprocess.check_call(["python", '-m', 'pip', 'install', 'geehydro'])

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
try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize()

# %%
'''
## Add layers to map
'''

# %%
Map = folium.Map()
Map.setOptions()

# Load an image.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')

# Center the map and display the image.
Map.setCenter(-122.1899, 37.5010, 10) # San Francisco Bay
Map.addLayer(image, {}, 'default color composite')

Map.setControlVisibility()
Map

# %%
'''
## RGB composites
The following illustrates the use of parameters to style a Landsat 8 image as a false-color composite:
'''

# %%
# Create a default map
Map = folium.Map()
Map.setOptions()

# Load an image.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')

# Define the visualization parameters.
vizParams = {
  'bands': ['B5', 'B4', 'B3'],
  'min': 0,
  'max': 0.5,
  'gamma': [0.95, 1.1, 1]
}

# Center the map and display the image.
Map.setCenter(-122.1899, 37.5010, 10) # San Francisco Bay
Map.addLayer(image, vizParams, 'false color composite')

# Display the map
Map.setControlVisibility()
Map

# %%
'''
## Color palettes
To display a single band of an image in color, set the `parameter` with a color ramp represented by a list of CSS-style color strings. (See this [reference](http://en.wikipedia.org/wiki/Web_colors) for more information). The following example illustrates how to use colors from cyan (`00FFFF`) to blue (`0000FF`) to render a [Normalized Difference Water Index (NDWI)](http://www.tandfonline.com/doi/abs/10.1080/01431169608948714) image.

In this example, note that the `min` and `max` parameters indicate the range of pixel values to which the palette should be applied. Intermediate values are linearly stretched. Also note that the `opt_show` parameter is set to `False`. This results in the visibility of the layer being off when it is added to the map. It can always be turned on again using the Layer Manager in the upper right corner of the map. The result should look something like below.
'''

# %%
# Create a default map
Map = folium.Map()
Map.setOptions()

#Load an image.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')

#Create an NDWI image, define visualization parameters and display.
ndwi = image.normalizedDifference(['B3', 'B5'])
ndwiViz = {'min': 0.5, 'max': 1, 'palette': ['00FFFF', '0000FF']}
Map.setCenter(-122.1899, 37.5010, 10) # San Francisco Bay
Map.addLayer(ndwi, ndwiViz, 'NDWI', False)

# Display the map
Map.setControlVisibility()
Map

# %%
'''
## Masking
You can use `image.updateMask()` to set the opacity of individual pixels based on where pixels in a mask image are non-zero. Pixels equal to zero in the mask are excluded from computations and the opacity is set to 0 for display. The following example uses an NDWI threshold (see the [Relational Operations section](https://developers.google.com/earth-engine/image_relational.html) for information on thresholds) to update the mask on the NDWI layer created previously:
'''

# %%
# Create a default map
Map = folium.Map()
Map.setOptions()

#Load an image.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')

#Create an NDWI image, define visualization parameters and display.
ndwi = image.normalizedDifference(['B3', 'B5'])
ndwiViz = {'min': 0.5, 'max': 1, 'palette': ['00FFFF', '0000FF']}
Map.setCenter(-122.1899, 37.5010, 10) # San Francisco Bay
Map.addLayer(ndwi, ndwiViz, 'NDWI', False)

# Mask the non-watery parts of the image, where NDWI < 0.4.
ndwiMasked = ndwi.updateMask(ndwi.gte(0.4))
Map.addLayer(ndwiMasked, ndwiViz, 'NDWI masked')

# Display the map
Map.setControlVisibility()
Map

# %%
'''
## Visualization images
Use the `image.visualize()` method to convert an image into an 8-bit RGB image for display or export. For example, to convert the false-color composite and NDWI to 3-band display images, use:
'''

# %%
# Create a default map
Map = folium.Map()
Map.setOptions()

#Load an image.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')

#Create an NDWI image, define visualization parameters and display.
ndwi = image.normalizedDifference(['B3', 'B5'])
ndwiViz = {'min': 0.5, 'max': 1, 'palette': ['00FFFF', '0000FF']}
Map.setCenter(-122.1899, 37.5010, 10) # San Francisco Bay
Map.addLayer(ndwi, ndwiViz, 'NDWI', False)

# Mask the non-watery parts of the image, where NDWI < 0.4.
ndwiMasked = ndwi.updateMask(ndwi.gte(0.4));
Map.addLayer(ndwiMasked, ndwiViz, 'NDWI masked', False)

# Create visualization layers.
imageRGB = image.visualize(**{'bands': ['B5', 'B4', 'B3'], 'max': 0.5})
ndwiRGB = ndwiMasked.visualize(**{
  'min': 0.5,
  'max': 1,
  'palette': ['00FFFF', '0000FF']
})

Map.addLayer(imageRGB, {}, 'imageRGB')
Map.addLayer(ndwiRGB, {}, 'ndwiRGB')

# Display the map
Map.setControlVisibility()
Map

# %%
'''
## Mosaicking
You can use masking and `imageCollection.mosaic()` (see the [Mosaicking section](https://developers.google.com/earth-engine/ic_composite_mosaic.html) for information on mosaicking) to achieve various cartographic effects. The `mosaic()` method renders layers in the output image according to their order in the input collection. The following example uses `mosaic()` to combine the masked NDWI and the false color composite and obtain a new visualization.

In this example, observe that a list of the two visualization images is provided to the ImageCollection constructor. The order of the list determines the order in which the images are rendered on the map. The result should look something like below.
'''

# %%
# Create a default map
Map = folium.Map()
Map.setOptions()

#Load an image.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')

#Create an NDWI image, define visualization parameters and display.
ndwi = image.normalizedDifference(['B3', 'B5'])
ndwiViz = {'min': 0.5, 'max': 1, 'palette': ['00FFFF', '0000FF']}
Map.setCenter(-122.1899, 37.5010, 10) # San Francisco Bay
Map.addLayer(ndwi, ndwiViz, 'NDWI', False)

# Mask the non-watery parts of the image, where NDWI < 0.4.
ndwiMasked = ndwi.updateMask(ndwi.gte(0.4));
Map.addLayer(ndwiMasked, ndwiViz, 'NDWI masked', False)

# Create visualization layers.
imageRGB = image.visualize(**{'bands': ['B5', 'B4', 'B3'], 'max': 0.5})
ndwiRGB = ndwiMasked.visualize(**{
  'min': 0.5,
  'max': 1,
  'palette': ['00FFFF', '0000FF']
})

Map.addLayer(imageRGB, {}, 'imageRGB', False)
Map.addLayer(ndwiRGB, {}, 'ndwiRGB', False)

# Mosaic the visualization layers and display (or export).
mosaic = ee.ImageCollection([imageRGB, ndwiRGB]).mosaic()
Map.addLayer(mosaic, {}, 'mosaic');

# Display the map
Map.setControlVisibility()
Map

# %%
'''
## Clipping
The `image.clip()` method is useful for achieving cartographic effects. The following example clips the mosaic shown above to an arbitrary buffer zone around the city of San Francisco.

Note that the coordinates are provided to the `Geometry` constructor and the buffer length is specified as 20,000 meters. Learn more about geometries on the [Geometries page](https://developers.google.com/earth-engine/geometries). The result, shown with the map in the background, should look something like below.
'''

# %%
# Create a default map
Map = folium.Map()
Map.setOptions()

#Load an image.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')

#Create an NDWI image, define visualization parameters and display.
ndwi = image.normalizedDifference(['B3', 'B5'])
ndwiViz = {'min': 0.5, 'max': 1, 'palette': ['00FFFF', '0000FF']}
Map.setCenter(-122.4344, 37.7599, 10) # San Francisco Bay
Map.addLayer(ndwi, ndwiViz, 'NDWI', False)

# Mask the non-watery parts of the image, where NDWI < 0.4.
ndwiMasked = ndwi.updateMask(ndwi.gte(0.4));
Map.addLayer(ndwiMasked, ndwiViz, 'NDWI masked', False)

# Create visualization layers.
imageRGB = image.visualize(**{'bands': ['B5', 'B4', 'B3'], 'max': 0.5})
ndwiRGB = ndwiMasked.visualize(**{
  'min': 0.5,
  'max': 1,
  'palette': ['00FFFF', '0000FF']
})

Map.addLayer(imageRGB, {}, 'imageRGB', False)
Map.addLayer(ndwiRGB, {}, 'ndwiRGB', False)

# Mosaic the visualization layers and display (or export).
mosaic = ee.ImageCollection([imageRGB, ndwiRGB]).mosaic()
Map.addLayer(mosaic, {}, 'mosaic', False);

# Create a circle by drawing a 20000 meter buffer around a point.
roi = ee.Geometry.Point([-122.4481, 37.7599]).buffer(20000)
clipped = mosaic.clip(roi)

# Display a clipped version of the mosaic.
Map.addLayer(clipped, {}, 'Clipped image')

# Display the map
Map.setControlVisibility()
Map

# %%
'''
## Rendering categorical maps
Palettes are also useful for rendering discrete valued maps, for example a land cover map. In the case of multiple classes, use the palette to supply a different color for each class. (The `image.remap()` method may be useful in this context, to convert arbitrary labels to consecutive integers). The following example uses a palette to render land cover categories:
'''

# %%
# Create a default map
Map = folium.Map()
Map.setOptions()

#Load 2012 MODIS land cover and select the IGBP classification.
cover = ee.Image('MODIS/051/MCD12Q1/2012_01_01') \
  .select('Land_Cover_Type_1')

#Define a palette for the 18 distinct land cover classes.
igbpPalette = [
  'aec3d4', #water
  '152106', '225129', '369b47', '30eb5b', '387242', #forest
  '6a2325', 'c3aa69', 'b76031', 'd9903d', '91af40',  #shrub, grass
  '111149', #wetlands
  'cdb33b', #croplands
  'cc0013', #urban
  '33280d', #crop mosaic
  'd7cdcc', #snow and ice
  'f7e084', #barren
  '6f6f6f'  #tundra
]

#Specify the min and max labels and the color palette matching the labels.
Map.setCenter(-99.229, 40.413, 5)
Map.addLayer(cover, {'min': 0, 'max': 17, 'palette': igbpPalette}, 'IGBP classification')

Map.setControlVisibility()
Map

# %%
'''
## Thumbnail images
Use the `ee.Image.getThumbURL()` method to generate a PNG or JPEG thumbnail image for an `ee.Image` object. Printing the outcome of an expression ending with a call to `getThumbURL()` results in a URL being printed to the console. Visiting the URL sets Earth Engine servers to work on generating the requested thumbnail on-the-fly. The image is displayed in the browser when processing completes. It can be downloaded by selecting appropriate options from the image’s right-click context menu.

The `getThumbURL()` method shares parameters with `Map.addLayer()`, described in the [visualization parameters table](https://developers.google.com/earth-engine/image_visualization#mapVisParamTable) above. Additionally, it takes optional `dimension`, `region`, and `crs` arguments that control the spatial extent, size, and display projection of the thumbnail.

![](https://i.imgur.com/eGNcPoN.png)

A single-band image will default to grayscale unless a `palette` argument is supplied. A multi-band image will default to RGB visualization of the first three bands, unless a `bands` argument is supplied. If only two bands are provided, the first band will map to red, the second to blue, and the green channel will be zero filled.

The following are a series of examples demonstrating various combinations of `getThumbURL()` parameter arguments. Visit the URLs printed to the console when you run this script to view the thumbnails.
'''

# %%
# Fetch a digital elevation model.
image = ee.Image('CGIAR/SRTM90_V4')

# Request a default thumbnail of the DEM with defined linear stretch.
# Set masked pixels (ocean) to 1000 so they map as gray.
thumbnail1 = image.unmask(1000).getThumbURL({
  'min': 0,
  'max': 3000,
  'dimensions': 500
})
print('Default extent and size:', thumbnail1)

# Specify region by GeoJSON, define palette, set size of the larger aspect dimension.
thumbnail2 = image.getThumbURL({
  'min': 0,
  'max': 3000,
  'palette': ['00A600','63C600','E6E600','E9BD3A','ECB176','EFC2B3','F2F2F2'],
  'dimensions': 500,
  'region': ee.Geometry.Rectangle([-84.6, -55.9, -32.9, 15.7]),
})
print('GeoJSON region, palette, and max dimension:', thumbnail2)

# %%
