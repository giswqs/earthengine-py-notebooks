import ee
from ee_plugin import Map



collection = ee.ImageCollection('USDA/NAIP/DOQQ')
fromFT = ee.FeatureCollection('ft:1CLldB-ULPyULBT2mxoRNv7enckVF0gCQoD2oH7XP')
polys = fromFT.geometry()
centroid = polys.centroid()
lng, lat = centroid.getInfo()['coordinates']
# print("lng = {}, lat = {}".format(lng, lat))

# lng_lat = ee.Geometry.Point(lng, lat)
naip = collection.filterBounds(polys)
naip_2015 = naip.filterDate('2015-01-01', '2015-12-31')
ppr = naip_2015.mosaic().clip(polys)

# print(naip_2015.size().getInfo())   # count = 120
vis = {'bands': ['N', 'R', 'G']}
Map.setCenter(lng, lat, 10)
# Map.addLayer(naip_2015,vis)
Map.addLayer(ppr,vis)
# Map.addLayer(fromFT)

ndwi = ppr.normalizedDifference(['G', 'N'])
ndwiViz = {'min': 0, 'max': 1, 'palette': ['00FFFF', '0000FF']}
ndwiMasked = ndwi.updateMask(ndwi.gte(0.05))
ndwi_bin = ndwiMasked.gt(0)
Map.addLayer(ndwiMasked, ndwiViz)

patch_size = ndwi_bin.connectedPixelCount(256, True)
# Map.addLayer(patch_size)

patch_id = ndwi_bin.connectedComponents(ee.Kernel.plus(1), 256)
Map.addLayer(patch_id)