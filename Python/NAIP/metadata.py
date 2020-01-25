import ee
from ee_plugin import Map



# fc = (ee.FeatureCollection('ft:1fRY18cjsHzDgGiJiS2nnpUU3v9JPDc2HNaR7Xk8')
#       .filter(ee.Filter().eq('Name', 'Minnesota')))

def print_image_id(image):
    index = image.get('system:time_start')
    print(index.getInfo())


lat = 46.80514
lng = -99.22023
lng_lat = ee.Geometry.Point(lng, lat)

collection = ee.ImageCollection('USDA/NAIP/DOQQ')
naip = collection.filterBounds(lng_lat)
naip_2015 = naip.filterDate('2010-01-01', '2015-12-31')

# print(naip_2015.getInfo())
# print(naip_2015.map(print_image_id))
# Map.setCenter(lon, lat, 13)
# Map.addLayer(naip_2015)


image = ee.Image('USDA/NAIP/DOQQ/m_4609915_sw_14_1_20100629')
bandNames = image.bandNames()
print('Band names: ', bandNames.getInfo())

b_nir = image.select('N')

proj = b_nir.projection()
print('Projection: ', proj.getInfo())

props = b_nir.propertyNames()
print(props.getInfo())

img_date = ee.Date(image.get('system:time_start'))
print('Timestamp: ', img_date.getInfo())

id = image.get('system:index')
print(id.getInfo())

# print(image.getInfo())

vis = {'bands': ['N', 'R', 'G']}
# Map.setCenter(lng, lat, 12)
# Map.addLayer(image,vis)


size = naip_2015.toList(100).length()
print("Number of images: ", size.getInfo())

count = naip_2015.size()
print("Count: ", count.getInfo())

dates = ee.List(naip_2015.get('date_range'))
date_range = ee.DateRange(dates.get(0),dates.get(1))
print("Date range: ", date_range.getInfo())
