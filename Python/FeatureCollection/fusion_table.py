import ee
from ee_plugin import Map



fromFT = ee.FeatureCollection('ft:1CLldB-ULPyULBT2mxoRNv7enckVF0gCQoD2oH7XP')
# print(fromFT.getInfo())

polys = fromFT.geometry()

centroid = polys.centroid()
print(centroid.getInfo())
lng, lat = centroid.getInfo()['coordinates']
print("lng = {}, lat = {}".format(lng, lat))

collection = ee.ImageCollection('LANDSAT/LC8_L1T_TOA')

path = collection.filterBounds(fromFT)

images = path.filterDate('2016-05-01', '2016-10-31')
print(images.size().getInfo())

median = images.median()

# lat = 46.80514
# lng = -99.22023
lng_lat = ee.Geometry.Point(lng, lat)
Map.setCenter(lng, lat, 10)
vis = {'bands': ['B5', 'B4', 'B3'], 'max': 0.3}
Map.addLayer(median,vis)
Map.addLayer(fromFT)