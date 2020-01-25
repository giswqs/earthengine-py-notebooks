import ee
from ee_plugin import Map



fromFT = ee.FeatureCollection('ft:1CLldB-ULPyULBT2mxoRNv7enckVF0gCQoD2oH7XP')
polys = fromFT.geometry()
centroid = polys.centroid()
lng, lat = centroid.getInfo()['coordinates']
# print("lng = {}, lat = {}".format(lng, lat))
# Map.setCenter(lng, lat, 10)
# Map.addLayer(fromFT)

count = fromFT.size().getInfo()
Map.setCenter(lng, lat, 10)

for i in range(2, 2 + count):
    fc = fromFT.filter(ee.Filter.eq('system:index', str(i)))
    Map.addLayer(fc)