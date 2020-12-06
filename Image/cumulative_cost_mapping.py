# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/Image/cumulative_cost_mapping.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/Image/cumulative_cost_mapping.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/Image/cumulative_cost_mapping.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
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
# A rectangle representing Bangui, Central African Republic.
geometry = ee.Geometry.Rectangle([18.5229, 4.3491, 18.5833, 4.4066])

# Create a source image where the geometry is 1, everything else is 0.
sources = ee.Image().toByte().paint(geometry, 1)

# Mask the sources image with itself.
sources = sources.updateMask(sources)

# The cost data is generated from classes in ESA/GLOBCOVER.
cover = ee.Image('ESA/GLOBCOVER_L4_200901_200912_V2_3').select(0)

# Classes 60, 80, 110, 140 have cost 1.
# Classes 40, 90, 120, 130, 170 have cost 2.
# Classes 50, 70, 150, 160 have cost 3.
cost = \
  cover.eq(60).Or(cover.eq(80)).Or(cover.eq(110)).Or(cover.eq(140)) \
      .multiply(1).add(
  cover.eq(40).Or(cover.eq(90)).Or(cover.eq(120)).Or(cover.eq(130)) \
    .Or(cover.eq(170)) \
      .multiply(2).add(
  cover.eq(50).Or(cover.eq(70)).Or(cover.eq(150)).Or(cover.eq(160)) \
      .multiply(3)))

# Compute the cumulative cost to traverse the lAnd cover.
cumulativeCost = cost.cumulativeCost(**{
  'source': sources,
  'maxDistance': 80 * 1000 # 80 kilometers
})

# Display the results
Map.setCenter(18.71, 4.2, 9)
Map.addLayer(cover, {}, 'Globcover')
Map.addLayer(cumulativeCost, {'min': 0, 'max': 5e4}, 'accumulated cost')
Map.addLayer(geometry, {'color': 'FF0000'}, 'source geometry')


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map