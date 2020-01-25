import ee
from ee_plugin import Map

# traditional python string
print('Hello world!')

# Earth Eninge object
print(ee.String('Hello World from Earth Engine!').getInfo())
print(ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318').getInfo())
