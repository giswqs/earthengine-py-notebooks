import ee
from ee_plugin import Map



collection = ee.ImageCollection('USDA/NAIP/DOQQ')

polys = ee.Geometry.Polygon(
        [[[-99.29615020751953, 46.725459351792374],
          [-99.2116928100586, 46.72404725733022],
          [-99.21443939208984, 46.772037733479884],
          [-99.30267333984375, 46.77321343419932]]])

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
# vis = {'bands': ['N', 'R', 'G']}
# Map.setCenter(lng, lat, 12)
# Map.addLayer(ppr,vis)
# Map.addLayer(polys)

downConfig = {'scale': 30, "maxPixels": 1.0E13, 'driveFolder': 'image'}  # scale means resolution.
img_lst = naip_2015.toList(100)

for i in range(0, count):
    image = ee.Image(img_lst.get(i))
    name = image.get('system:index').getInfo()
    # print(name)
    task = ee.batch.Export.image(image, name, downConfig)
    task.start()

