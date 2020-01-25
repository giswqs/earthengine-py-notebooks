import ee 
from ee_plugin import Map 

# This function adds a band representing the image timestamp.
def addTime(image): 
  return image.addBands(image.metadata('system:time_start'))

def conditional(image):
  return ee.Algorithms.If(ee.Number(image.get('SUN_ELEVATION')).gt(40),
                            image,
                            ee.Image(0))

# Load a Landsat 8 collection for a single path-row.
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
  .filter(ee.Filter.eq('WRS_PATH', 44)) \
  .filter(ee.Filter.eq('WRS_ROW', 34))



# Map the function over the collection and display the result.
print(collection.map(addTime).getInfo())


# Load a Landsat 8 collection for a single path-row.
collection = ee.ImageCollection('LANDSAT/LC8_L1T_TOA') \
  .filter(ee.Filter.eq('WRS_PATH', 44)) \
  .filter(ee.Filter.eq('WRS_ROW', 34))

# This function uses a conditional statement to return the image if
# the solar elevation > 40 degrees.  Otherwise it returns a zero image.
# conditional = function(image) {
#   return ee.Algorithms.If(ee.Number(image.get('SUN_ELEVATION')).gt(40),
#                           image,
#                           ee.Image(0))
# }

# Map the function over the collection, convert to a List and print the result.
print('Expand this to see the result: ', collection.map(conditional).getInfo())

