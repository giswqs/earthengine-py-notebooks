import ee


image1 = ee.Image(1)
print(image1)
print(image1.getInfo())

image2 = ee.Image(2)
image3 = ee.Image.cat([image1, image2])
print(image3.getInfo())

multiband = ee.Image([1, 2, 3])
print(multiband)
renamed = multiband.select(['constant','constant_1','constant_2'],['band1','band2','band3'])
print(renamed)