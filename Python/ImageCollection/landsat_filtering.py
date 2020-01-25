import ee
from ee_plugin import Map

collection = ee.ImageCollection('LANDSAT/LC8_L1T_TOA')

path = collection.filter(ee.Filter.eq('WRS_PATH', 44))
row = path.filter(ee.Filter.eq('WRS_ROW', 34))

images = row.filterDate('2016-01-01', '2016-12-31')
print(images.size().getInfo())
# images.map(lambda image: image.getInfo())

lng = -122.3578
lat = 37.7726

median = images.median()
Map.setCenter(lng, lat, 12)
vis = {'bands': ['B5', 'B4', 'B3'], 'max': 0.3}
Map.addLayer(median, vis)
