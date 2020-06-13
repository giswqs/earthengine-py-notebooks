# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/JavaScripts/Image/CenterPivotIrrigationDetector.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/JavaScripts/Image/CenterPivotIrrigationDetector.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/JavaScripts/Image/CenterPivotIrrigationDetector.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
</table>
"""

# %%
"""
## Install Earth Engine API and geemap
Install the [Earth Engine Python API](https://developers.google.com/earth-engine/python_install) and [geemap](https://github.com/giswqs/geemap). The **geemap** Python package is built upon the [ipyleaflet](https://github.com/jupyter-widgets/ipyleaflet) and [folium](https://github.com/python-visualization/folium) packages and implements several methods for interacting with Earth Engine data layers, such as `Map.addLayer()`, `Map.setCenter()`, and `Map.centerObject()`.
The following script checks if the geemap package has been installed. If not, it will install geemap, which automatically installs its [dependencies](https://github.com/giswqs/geemap#dependencies), including earthengine-api, folium, and ipyleaflet.

**Important note**: A key difference between folium and ipyleaflet is that ipyleaflet is built upon ipywidgets and allows bidirectional communication between the front-end and the backend enabling the use of the map to capture user input, while folium is meant for displaying static data only ([source](https://blog.jupyter.org/interactive-gis-in-jupyter-with-ipyleaflet-52f9657fa7a)). Note that [Google Colab](https://colab.research.google.com/) currently does not support ipyleaflet ([source](https://github.com/googlecolab/colabtools/issues/60#issuecomment-596225619)). Therefore, if you are using geemap with Google Colab, you should use [`import geemap.eefolium`](https://github.com/giswqs/geemap/blob/master/geemap/eefolium.py). If you are using geemap with [binder](https://mybinder.org/) or a local Jupyter notebook server, you can use [`import geemap`](https://github.com/giswqs/geemap/blob/master/geemap/geemap.py), which provides more functionalities for capturing user input (e.g., mouse-clicking and moving).
"""

# %%
# Installs geemap package
import subprocess

try:
    import geemap
except ImportError:
    print('geemap package not installed. Installing ...')
    subprocess.check_call(["python", '-m', 'pip', 'install', 'geemap'])

# Checks whether this notebook is running on Google Colab
try:
    import google.colab
    import geemap.eefolium as geemap
except:
    import geemap

# Authenticates and initializes Earth Engine
import ee

try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize()  

# %%
"""
## Create an interactive map 
The default basemap is `Google MapS`. [Additional basemaps](https://github.com/giswqs/geemap/blob/master/geemap/basemaps.py) can be added using the `Map.add_basemap()` function. 
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
# Center-pivot Irrigation Detector.
#
# Finds circles that are 500m in radius.
Map.setCenter(-106.06, 37.71, 12)

# A nice NDVI palette.
palette = [
  'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718',
  '74A901', '66A000', '529400', '3E8601', '207401', '056201',
  '004C00', '023B01', '012E01', '011D01', '011301']

# Just display the image with the palette.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_034034_20170608')
ndvi = image.normalizedDifference(['B5','B4'])

Map.addLayer(ndvi, {'min': 0, 'max': 1, 'palette': palette}, 'Landsat NDVI')

# Find the difference between convolution with circles and squares.
# This difference, in theory, will be strongest at the center of
# circles in the image. This region is filled with circular farms
# with radii on the order of 500m.
farmSize = 500;  # Radius of a farm, in meters.
circleKernel = ee.Kernel.circle(farmSize, 'meters')
squareKernel = ee.Kernel.square(farmSize, 'meters')
circles = ndvi.convolve(circleKernel)
squares = ndvi.convolve(squareKernel)
diff = circles.subtract(squares)

# Scale by 100 and find the best fitting pixel in each neighborhood.
diff = diff.abs().multiply(100).toByte()
max = diff.focal_max({'radius': farmSize * 1.8, 'units': 'meters'})
# If a pixel isn't the local max, set it to 0.
local = diff.where(diff.neq(max), 0)
thresh = local.gt(2)

# Here, we highlight the maximum differences as "Kernel Peaks"
# and draw them in red.
peaks = thresh.focal_max({'kernel': circleKernel})
Map.addLayer(peaks.updateMask(peaks), {'palette': 'FF3737'}, 'Kernel Peaks')

# Detect the edges of the features.  Discard the edges with lower intensity.
canny = ee.Algorithms.CannyEdgeDetector(ndvi, 0)
canny = canny.gt(0.3)

# Create a "ring" kernel from two circular kernels.
inner = ee.Kernel.circle(farmSize - 20, 'meters', False, -1)
outer = ee.Kernel.circle(farmSize + 20, 'meters', False, 1)
ring = outer.add(inner, True)

# Highlight the places where the feature edges best match the circle kernel.
centers = canny.convolve(ring).gt(0.5).focal_max({'kernel': circleKernel})
Map.addLayer(centers.updateMask(centers), {'palette': '4285FF'}, 'Ring centers')


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map