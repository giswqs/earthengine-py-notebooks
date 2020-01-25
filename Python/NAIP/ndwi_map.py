import ee
from ee_plugin import Map



collection = ee.ImageCollection('USDA/NAIP/DOQQ')
fromFT = ee.FeatureCollection('ft:1CLldB-ULPyULBT2mxoRNv7enckVF0gCQoD2oH7XP')
polys = fromFT.geometry()
# polys = ee.Geometry.Polygon(
#         [[[-99.29615020751953, 46.725459351792374],
#           [-99.2116928100586, 46.72404725733022],
#           [-99.21443939208984, 46.772037733479884],
#           [-99.30267333984375, 46.77321343419932]]])

centroid = polys.centroid()
lng, lat = centroid.getInfo()['coordinates']
print("lng = {}, lat = {}".format(lng, lat))

lng_lat = ee.Geometry.Point(lng, lat)
naip = collection.filterBounds(polys)
naip_2015 = naip.filterDate('2015-01-01', '2015-12-31')
ppr = naip_2015.mosaic()

count = naip_2015.size().getInfo()
print("Count: ", count)

# print(naip_2015.size().getInfo())
vis = {'bands': ['N', 'R', 'G']}
Map.setCenter(lng, lat, 12)
Map.addLayer(ppr,vis)
# Map.addLayer(polys)

def NDWI(image):
    """A function to compute NDWI."""
    ndwi = image.normalizedDifference(['G', 'N'])
    ndwiViz = {'min': 0, 'max': 1, 'palette': ['00FFFF', '0000FF']}
    ndwiMasked = ndwi.updateMask(ndwi.gte(0.05))
    ndwi_bin = ndwiMasked.gt(0)
    patch_size = ndwi_bin.connectedPixelCount(500, True)
    large_patches = patch_size.eq(500)
    large_patches = large_patches.updateMask(large_patches)
    opened = large_patches.focal_min(1).focal_max(1)
    return opened

ndwi_collection = naip_2015.map(NDWI)
# Map.addLayer(ndwi_collection)
# print(ndwi_collection.getInfo())

# downConfig = {'scale': 10, "maxPixels": 1.0E13, 'driveFolder': 'image'}  # scale means resolution.
# img_lst = ndwi_collection.toList(100)
#
# taskParams = {
#     'driveFolder': 'image',
#     'driveFileNamePrefix': 'ndwi',
#     'fileFormat': 'KML'
# }
#
# for i in range(0, count):
#     image = ee.Image(img_lst.get(i))
#     name = image.get('system:index').getInfo()
#     print(name)
#     # task = ee.batch.Export.image(image, "ndwi2-" + name, downConfig)
#     # task.start()

mosaic = ndwi_collection.mosaic().clip(polys)
fc = mosaic.reduceToVectors(eightConnected=True, maxPixels=59568116121, crs=mosaic.projection(), scale=1)
# Map.addLayer(fc)
taskParams = {
    'driveFolder': 'image',
    'driveFileNamePrefix': 'water',
    'fileFormat': 'KML'
}

count = fromFT.size().getInfo()
Map.setCenter(lng, lat, 10)

for i in range(2, 2 + count):
    watershed = fromFT.filter(ee.Filter.eq('system:index', str(i)))
    re = fc.filterBounds(watershed)
    task = ee.batch.Export.table(re, 'watershed-' + str(i), taskParams)
    task.start()
    # Map.addLayer(fc)


# lpc = fromFT.filter(ee.Filter.eq('name', 'Little Pipestem Creek'))
