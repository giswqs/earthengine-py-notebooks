import ee 
from ee_plugin import Map 

# Load a Landsat 8 ImageCollection for a single path-row.
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
    .filter(ee.Filter.eq('WRS_PATH', 44)) \
    .filter(ee.Filter.eq('WRS_ROW', 34)) \
    .filterDate('2014-03-01', '2014-08-01')
print('Collection: ', collection.getInfo())

# Get the number of images.
count = collection.size()
print('Count: ', count.getInfo())

# Get the date range of images in the collection.
range = collection.reduceColumns(ee.Reducer.minMax(), ["system:time_start"])
print('Date range: ', ee.Date(range.get('min')).getInfo(), ee.Date(range.get('max')).getInfo())

# Get statistics for a property of the images in the collection.
sunStats = collection.aggregate_stats('SUN_ELEVATION')
print('Sun elevation statistics: ', sunStats.getInfo())

# Sort by a cloud cover property, get the least cloudy image.
image = ee.Image(collection.sort('CLOUD_COVER').first())
print('Least cloudy image: ', image.getInfo())

# Limit the collection to the 10 most recent images.
recent = collection.sort('system:time_start', False).limit(10)
print('Recent images: ', recent.getInfo())

