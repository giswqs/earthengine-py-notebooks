# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Image/set_image_properties.py

import ee
from ee_plugin import Map


def addDate(image):
    # parse date stored in 'system:index'
    date = ee.Date(image.get('system:index'))

    # format date, see http:#www.joda.org/joda-time/apidocs/org/joda/time/format/DateTimeFormat.html
    str = date.format('YYYY-mm-dd')

    return image.set({'Date': str})


# point = ee.Geometry.Point(-122.262, 37.8719)
# start = ee.Date('2014-06-01')
# finish = ee.Date('2014-10-01')

# filteredCollection = ee.ImageCollection('LANDSAT/LC08/C01/T1') \
#     .filterBounds(point) \
#     .filterDate(start, finish) \
#     .sort('CLOUD_COVER', True)

filteredCollection = ee.ImageCollection('users/sdavidcomer/L7maskedNDVIdated')

# Bring in image collection
# ndvi = ee.ImageCollection('users/sdavidcomer/L7maskedNDVIdated')

# Map addDate over image collection
result = filteredCollection.map(addDate)
print(result.first().get('Date').getInfo())
