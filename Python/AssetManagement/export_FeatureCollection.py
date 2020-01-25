import ee
from ee_plugin import Map



fromFT = ee.FeatureCollection('ft:1CLldB-ULPyULBT2mxoRNv7enckVF0gCQoD2oH7XP')
polys = fromFT.geometry()
centroid = polys.centroid()
lng, lat = centroid.getInfo()['coordinates']
print("lng = {}, lat = {}".format(lng, lat))
Map.setCenter(lng, lat, 10)
Map.addLayer(fromFT)

taskParams = {
    'driveFolder': 'image',
    'fileFormat': 'KML'   # CSV, KMZ, GeoJSON
}

# export all features in a FeatureCollection as one file
task = ee.batch.Export.table(fromFT, 'export_fc', taskParams)
task.start()

# # export each feature in a FeatureCollection as an individual file
# count = fromFT.size().getInfo()
# for i in range(2, 2 + count):
#     fc = fromFT.filter(ee.Filter.eq('system:index', str(i)))
#     task = ee.batch.Export.table(fc, 'watershed-' + str(i), taskParams)
#     task.start()
