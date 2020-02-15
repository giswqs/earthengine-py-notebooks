# %%
'''
# Get Started with Earth Engine

This Get Started guide is intended as a quick way to start programming with the Earth Engine Python API. For an introductory look at Python and more in-depth exercises with the Earth Engine API, see the [tutorials](https://github.com/giswqs/earthengine-py-notebooks). For suggestions on Python coding style, see the [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html).[link text](https://)

Google Earth Engine allows users to run algorithms on georeferenced imagery and vectors stored on Google's infrastructure. The Google Earth Engine API provides a library of functions which may be applied to data for display and analysis. Earth Engine's [public data catalog](https://developers.google.com/earth-engine/datasets/) contains a large amount of publicly available imagery and vector datasets. Private assets can also be created in users' personal folders.

'''

# %%
'''
## Installing the Earth Engine API
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
# ee.Authenticate()
ee.Initialize()

# %%
'''
## ‘Hello world!’
Printing out information to the console is a basic task for getting information about an object, displaying the numeric result of a computation, displaying object metadata or helping with debugging. The iconic ‘Hello World!’ example is:
'''

# %%
# traditional python string
print('Hello world!')

# %%
# Earth Eninge object
print(ee.String('Hello World from Earth Engine!').getInfo())

# %%
print(ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318').getInfo())

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
## Adding data to the map
In addition to printing information to the console, adding data to the Map is the way to visualize geographic data. Use Map.addLayer() to do that. In the following example, an Image is instantiated (how to find these images is covered later) using ee.Image(), added to the map with Map.addLayer() and the map is centered over the image:
'''

# %%
# Load an image.
image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318')

# Center the map on the image.
Map.centerObject(image, 9)

# Display the image.
Map.addLayer(image, {}, 'Landsat 8 original image')

# Define visualization parameters in an object literal.
vizParams = {'bands': ['B5', 'B4', 'B3'],
             'min': 5000, 'max': 15000, 'gamma': 1.3}

# Center the map on the image and display.
Map.centerObject(image, 9)
Map.addLayer(image, vizParams, 'Landsat 8 False color')

# Use Map.addLayer() to add features and feature collections to the map. For example,
counties = ee.FeatureCollection('TIGER/2016/Counties')
Map.addLayer(counties, {}, 'counties')

# %%
'''
## Display Earth Engine data layers 
'''

# %%
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map

# %%
'''
## Finding images, image collections and feature collections
Images, image collections, and feature collections are discoverable by searching the Earth Engine Data Catalog. For example, entering ‘Landsat 8’ into the search field results in a list of raster datasets. (The complete listing of Earth Engine datasets is at the [Earth Engine Data Catalog](https://developers.google.com/earth-engine/datasets)). Click on the dataset name to get a brief description, information about the temporal availability, data provider and collection ID. 
'''

# %%
# Create a map
Map = folium.Map(location=[40, -100], zoom_start=4)
Map.setOptions('HYBRID')

# Add Earth Engine script
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1')

point = ee.Geometry.Point(-122.262, 37.8719)
start = ee.Date('2014-06-01')
finish = ee.Date('2014-10-01')

filteredCollection = ee.ImageCollection('LANDSAT/LC08/C01/T1') \
    .filterBounds(point) \
    .filterDate(start, finish) \
    .sort('CLOUD_COVER', True)

first = filteredCollection.first()
# Define visualization parameters in an object literal.
vizParams = {'bands': ['B5', 'B4', 'B3'],
             'min': 5000, 'max': 15000, 'gamma': 1.3}
Map.centerObject(first, 8)
Map.addLayer(first, vizParams, 'Landsat 8 image')

# Load a feature collection.
featureCollection = ee.FeatureCollection('TIGER/2016/States')

# Filter the collection.
filteredFC = featureCollection.filter(ee.Filter.eq('NAME', 'California'))

# Create a mosiac
mosaic = ee.ImageCollection('LANDSAT/LC08/C01/T1') \
    .filterBounds(filteredFC) \
    .filterDate('2019-01-01', '2019-12-31') \

median = mosaic.median().clip(filteredFC)

Map.addLayer(median, vizParams, 'Median')

# Display the collection.
Map.addLayer(filteredFC, {}, 'California')

# Diplay the map
Map.setControlVisibility(layerControl=True, fullscreenControl=True, latLngPopup=True)
Map


# %%
'''
## Band math
Perform mathematical operations on images using Image methods. This may include band recombinations (spectral indices), image differencing or mathematical operations such as multiplication by a constant. For example, compute the difference between Normalized Difference Vegetation Index (NDVI) images 20 years apart:
'''

# %%
# This function gets NDVI from Landsat 5 imagery.
def getNDVI(image):
    return image.normalizedDifference(['B4', 'B3'])


# Load two Landsat 5 images, 20 years apart.
image1 = ee.Image('LANDSAT/LT05/C01/T1_TOA/LT05_044034_19900604')
image2 = ee.Image('LANDSAT/LT05/C01/T1_TOA/LT05_044034_20100611')

# Compute NDVI from the scenes.
ndvi1 = getNDVI(image1)
ndvi2 = getNDVI(image2)

# Compute the difference in NDVI.
ndviDifference = ndvi2.subtract(ndvi1)

ndviParams = {'palette': ['#d73027', '#f46d43', '#fdae61',
                          '#fee08b', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850']}
ndwiParams = {'min': -0.5, 'max': 0.5, 'palette': ['FF0000', 'FFFFFF', '0000FF']}

# Create a map
Map = folium.Map(location=[40, -100], zoom_start=4)
Map.setOptions('HYBRID')

Map.centerObject(image1, 10)
Map.addLayer(ndvi1, ndviParams, 'NDVI 1')
Map.addLayer(ndvi2, ndviParams, 'NDVI 2')
Map.addLayer(ndviDifference, ndwiParams, 'NDVI difference')

# Diplay the map
Map.setControlVisibility()
Map

# %%
'''
## Mapping (what to do instead of a for-loop)
Use `map()` to iterate over items in a collection. (For loops are NOT the right way to do that in Earth Engine and should be avoided). The `map()` function can be applied to an `ImageCollection`, a `FeatureCollection` or a `List` and accepts a function as its argument. The argument of the function is an element of the collection over which it is mapped. This is useful for modifying every element of the collection in the same way, for example adding. For example, the following code adds an NDVI band to every image in an `ImageCollection`:
'''

# %%
# This function gets NDVI from Landsat 8 imagery.

def addNDVI(image):
    return image.addBands(image.normalizedDifference(['B5', 'B4']))

# Load the Landsat 8 raw data, filter by location and date.
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1') \
    .filterBounds(ee.Geometry.Point(-122.262, 37.8719)) \
    .filterDate('2014-06-01', '2014-10-01')

# Map the function over the collection.
ndviCollection = collection.map(addNDVI)

first = ndviCollection.first()
print(first.getInfo())

bandNames = first.bandNames()
print(bandNames.getInfo())

# %%
'''
## Reducing
Reducing is the way to aggregate data over time, space, bands, arrays and other data structures in Earth Engine. Various methods exist for this purpose in the API. For example, to make a composite of an `ImageCollection`, use `reduce()` to reduce the images in the collection to one Image. A simple example is creating the median composite of the five least cloudy scenes in the Landsat 8 collection defined earlier:
'''

# %%
# Load a Landsat 8 collection.
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1') \
    .filterBounds(ee.Geometry.Point(-122.262, 37.8719)) \
    .filterDate('2014-01-01', '2014-12-31') \
    .sort('CLOUD_COVER')

# Compute the median of each pixel for each band of the 5 least cloudy scenes.
median = collection.limit(5).reduce(ee.Reducer.median())

# Define visualization parameters in an object literal.
vizParams = {'bands': ['B5_median', 'B4_median', 'B3_median'],
             'min': 5000, 'max': 15000, 'gamma': 1.3}

Map = folium.Map()
Map.setOptions('HYBRID')
Map.setCenter(-122.262, 37.8719, 10)
Map.addLayer(median, vizParams, 'Median image')
Map.setControlVisibility()
Map

# %%
'''
Reducing is also the way to get statistics of an image in the regions defined by a `Feature` or `FeatureCollection`. Suppose the task is to compute the mean pixel values within an area of interest. Use `reduceRegion()` for this purpose. For example:
'''

# %%
# Create a map
Map = folium.Map()
Map.setOptions('HYBRID')

# Load and display a Landsat TOA image.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')
Map.addLayer(image, {'bands': ['B4', 'B3', 'B2'], max: 0.3}, 'Landsat 8')

# // Create an arbitrary rectangle as a region and display it.
region = ee.Geometry.Rectangle(-122.2806, 37.1209, -122.0554, 37.2413)
Map.centerObject(region, 10)
Map.addLayer(region, {}, 'ROI')

# // Get a dictionary of means in the region.  Keys are bandnames.
mean = image.reduceRegion(**{
  'reducer': ee.Reducer.mean(),
  'geometry': region,
  'scale': 30
})

results = mean.getInfo()
for item in results.items():
  print(item)

Map.setControlVisibility()
Map

# %%
'''
## Masking
Every pixel in an `ee.Image` has both a value and a mask which ranges from 0 (no data) to 1. Masked pixels (in which mask==0) are treated as no data. Pixels with 0 < mask ≤ 1 have a value, but it is weighted by the mask for numerical computations.

You can make pixels transparent or exclude them from analysis using masks. Pixels are masked when the mask value is zero. Continuing the image differencing example, use a mask to display areas of increased and decreased NDVI over the difference interval:
'''

# %%
# This function gets NDVI from Landsat 5 imagery.
def getNDVI(image):
    return image.normalizedDifference(['B4', 'B3'])

# Load two Landsat 5 images, 20 years apart.
image1 = ee.Image('LANDSAT/LT05/C01/T1_TOA/LT05_044034_19900604')
image2 = ee.Image('LANDSAT/LT05/C01/T1_TOA/LT05_044034_20100611')

# Compute NDVI from the scenes.
ndvi1 = getNDVI(image1)
ndvi2 = getNDVI(image2)

# Compute the difference in NDVI.
ndviDifference = ndvi2.subtract(ndvi1)
# Load the land mask from the SRTM DEM.
landMask = ee.Image('CGIAR/SRTM90_V4').mask()

# Update the NDVI difference mask with the land mask.
maskedDifference = ndviDifference.updateMask(landMask)

# Display the masked result.
vizParams = {'min': -0.5, 'max': 0.5,
             'palette': ['FF0000', 'FFFFFF', '0000FF']}

Map = folium.Map()
Map.setOptions('HYBRID')
Map.setCenter(-122.2531, 37.6295, 9)
Map.addLayer(ndviDifference, vizParams, 'NDVI difference without mask', False)
Map.addLayer(maskedDifference, vizParams, 'NDVI difference with mask')
Map.setControlVisibility()
Map

# %%


# %%
'''
## A complete example
The following example demonstrates multiple concepts: filtering, mapping, reducing and the use of a cloud mask:
'''

# %%
# This function gets NDVI from a Landsat 8 image.

def addNDVI(image):
    return image.addBands(image.normalizedDifference(['B5', 'B4']))

# This function masks cloudy pixels.


def cloudMask(image):
    clouds = ee.Algorithms.Landsat.simpleCloudScore(image).select(['cloud'])
    return image.updateMask(clouds.lt(10))

# Create a map
Map = folium.Map()
Map.setOptions('HYBRID')

# Load a Landsat collection, map the NDVI and cloud masking functions over it.
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
    .filterBounds(ee.Geometry.Point([-122.262, 37.8719])) \
    .filterDate('2014-03-01', '2014-05-31') \
    .map(addNDVI) \
    .map(cloudMask)

# Reduce the collection to the mean of each pixel and display.
meanImage = collection.reduce(ee.Reducer.mean())
vizParams = {'bands': ['B5_mean', 'B4_mean', 'B3_mean'], 'min': 0, 'max': 0.5}
Map.setCenter(-122.262, 37.8719, 10)
Map.addLayer(meanImage, vizParams, 'mean')

# Load a region in which to compute the mean and display it.
counties = ee.FeatureCollection('TIGER/2016/Counties')
santaClara = ee.Feature(counties.filter(
    ee.Filter.eq('NAME', 'Santa Clara')).first())
Map.addLayer(ee.Image().paint(santaClara, 0, 2), {
             'palette': 'yellow'}, 'Santa Clara')

# Get the mean of NDVI in the region.
mean = meanImage.select(['nd_mean']).reduceRegion(**{
    'reducer': ee.Reducer.mean(),
    'geometry': santaClara.geometry(),
    'scale': 30
})

# Print mean NDVI for the region.
print('Santa Clara spring mean NDVI:', mean.get('nd_mean').getInfo())

Map.setControlVisibility()
Map

# %%
