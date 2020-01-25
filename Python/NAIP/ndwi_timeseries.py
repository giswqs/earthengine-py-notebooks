import ee
from ee_plugin import Map




def subsetNAIP(img_col, startTime, endTime, fc):
    img = img_col.filterDate(startTime, endTime).filterBounds(fc).mosaic().clip(fc)
    return img

def calNDWI(image, threshold):
    """A function to compute NDWI."""
    ndwi = image.normalizedDifference(['G', 'N'])
    ndwiViz = {'min': 0, 'max': 1, 'palette': ['00FFFF', '0000FF']}
    ndwiMasked = ndwi.updateMask(ndwi.gte(threshold))
    ndwi_bin = ndwiMasked.gt(0)
    patch_size = ndwi_bin.connectedPixelCount(500, True)
    large_patches = patch_size.eq(500)
    large_patches = large_patches.updateMask(large_patches)
    opened = large_patches.focal_min(1).focal_max(1)
    return opened

def rasterToVector(img, fc):
    vec = img.reduceToVectors(geometry=fc, eightConnected=True, maxPixels=59568116121, crs=img.projection(), scale=1)
    return vec

def exportToDrive(vec, filename):
    taskParams = {
        'driveFolder': 'image',
        'fileFormat': 'KML'
    }
    task = ee.batch.Export.table(vec, filename, taskParams)
    task.start()


years = [2014]
threshold = 0.3
# years = [2003, 2004, 2005, 2006, 2009, 2010, 2012, 2014, 2015]

collection = ee.ImageCollection('USDA/NAIP/DOQQ')
fromFT = ee.FeatureCollection('ft:1CLldB-ULPyULBT2mxoRNv7enckVF0gCQoD2oH7XP')
# count = fromFT.size().getInfo()
# print(count)
polys = fromFT.geometry()
centroid = polys.centroid()
lng, lat = centroid.getInfo()['coordinates']
# print("lng = {}, lat = {}".format(lng, lat))
values = fromFT.reduceColumns(ee.Reducer.toList(2), ['system:index', 'name']).getInfo()['list']
# print(values)
# Map.setCenter(lng, lat, 10)
vis = {'bands': ['N', 'R', 'G']}

for year in years:
    # year = 2015

    startTime = ee.Date(str(year) + '-01-01')
    endTime = ee.Date(str(year) + '-12-31')
    # year = startTime.get('year').getInfo()
    # print(year)

    for (id, name) in values:
        watershed = fromFT.filter(ee.Filter.eq('system:index', str(id)))
        filename = "Y" + str(year) + "_" + str(id) + "_" + str(name).replace(" ", "_")
        print(filename)
        image = subsetNAIP(collection, startTime, endTime, watershed)
        ndwi = calNDWI(image, threshold)
        vector = rasterToVector(ndwi, watershed)
        exportToDrive(vector, filename)
        # Map.addLayer(image, vis)
        # Map.addLayer(vector)


# for i in range(2, 2 + count):
#     watershed = fromFT.filter(ee.Filter.eq('system:index', str(i)))
#     re = fc.filterBounds(watershed)
    # task = ee.batch.Export.table(re, 'watershed-' + str(i), taskParams)
    # task.start()
    #


#
#
# lng_lat = ee.Geometry.Point(lng, lat)
# naip = collection.filterBounds(polys)
# naip_2015 = naip.filterDate('2015-01-01', '2015-12-31')
# ppr = naip_2015.mosaic()
#
# count = naip_2015.size().getInfo()
# print("Count: ", count)
#
# # print(naip_2015.size().getInfo())
# vis = {'bands': ['N', 'R', 'G']}
# Map.setCenter(lng, lat, 12)
# Map.addLayer(ppr,vis)
# # Map.addLayer(polys)
#
# def NDWI(image):
#     """A function to compute NDWI."""
#     ndwi = image.normalizedDifference(['G', 'N'])
#     ndwiViz = {'min': 0, 'max': 1, 'palette': ['00FFFF', '0000FF']}
#     ndwiMasked = ndwi.updateMask(ndwi.gte(0.05))
#     ndwi_bin = ndwiMasked.gt(0)
#     patch_size = ndwi_bin.connectedPixelCount(500, True)
#     large_patches = patch_size.eq(500)
#     large_patches = large_patches.updateMask(large_patches)
#     opened = large_patches.focal_min(1).focal_max(1)
#     return opened
#
# ndwi_collection = naip_2015.map(NDWI)
# # Map.addLayer(ndwi_collection)
# # print(ndwi_collection.getInfo())
#
# # downConfig = {'scale': 10, "maxPixels": 1.0E13, 'driveFolder': 'image'}  # scale means resolution.
# # img_lst = ndwi_collection.toList(100)
# #
# # taskParams = {
# #     'driveFolder': 'image',
# #     'driveFileNamePrefix': 'ndwi',
# #     'fileFormat': 'KML'
# # }
# #
# # for i in range(0, count):
# #     image = ee.Image(img_lst.get(i))
# #     name = image.get('system:index').getInfo()
# #     print(name)
# #     # task = ee.batch.Export.image(image, "ndwi2-" + name, downConfig)
# #     # task.start()
#
# mosaic = ndwi_collection.mosaic().clip(polys)
# fc = mosaic.reduceToVectors(eightConnected=True, maxPixels=59568116121, crs=mosaic.projection(), scale=1)
# # Map.addLayer(fc)
# taskParams = {
#     'driveFolder': 'image',
#     'driveFileNamePrefix': 'water',
#     'fileFormat': 'KML'
# }
#
# count = fromFT.size().getInfo()
# Map.setCenter(lng, lat, 10)
#
# for i in range(2, 2 + count):
#     watershed = fromFT.filter(ee.Filter.eq('system:index', str(i)))
#     re = fc.filterBounds(watershed)
#     # task = ee.batch.Export.table(re, 'watershed-' + str(i), taskParams)
#     # task.start()
#     # Map.addLayer(fc)
#
#
# # lpc = fromFT.filter(ee.Filter.eq('name', 'Little Pipestem Creek'))
