# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Image/band_stats.py

import ee
from ee_plugin import Map


# get highest value
def maxValue(img, scale=30):
    max_value = img.reduceRegion(**{
        'reducer': ee.Reducer.max(),
        'geometry': img.geometry(),
        'scale': scale,
        'maxPixels': 1e9
    })
    return max_value


# get lowest value
def minValue(img, scale=30):
    min_value = img.reduceRegion(**{
        'reducer': ee.Reducer.min(),
        'geometry': img.geometry(),
        'scale': scale,
        'maxPixels': 1e9
    })
    return min_value


# get mean value
def meanValue(img, scale=30):
    mean_value = img.reduceRegion(**{
        'reducer': ee.Reducer.mean(),
        'geometry': img.geometry(),
        'scale': scale,
        'maxPixels': 1e9
    })
    return mean_value


# get standard deviation
def stdValue(img, scale=30):
    std_value = img.reduceRegion(**{
        'reducer': ee.Reducer.stdDev(),
        'geometry': img.geometry(),
        'scale': scale,
        'maxPixels': 1e9
    })
    return std_value


dataset = ee.Image('USGS/NED')
dem = dataset.select('elevation')
# dem = ee.Image('srtm90_v4')
vis_params = {'min': 0, 'max': 3000}
Map.addLayer(dem, vis_params, 'NED', False)

roi = ee.Geometry.Polygon(
    [[[-120.18204899532924, 38.53481618819663],
      [-120.18204899532924, 36.54889033300136],
      [-116.75431462032924, 36.54889033300136],
      [-116.75431462032924, 38.53481618819663]]])

image = dem.clip(roi)
Map.centerObject(image, 9)
Map.addLayer(image, vis_params, 'DEM')

scale = image.projection().nominalScale()
print("Resolution: ", scale.getInfo())

scale = 30

print("Minimum value: ", minValue(image, scale).get('elevation').getInfo())
print("Maximum value: ", maxValue(image, scale).get('elevation').getInfo())
print("Average value: ", meanValue(image, scale).get('elevation').getInfo())
print("Standard deviation: ", stdValue(image, scale).get('elevation').getInfo())
