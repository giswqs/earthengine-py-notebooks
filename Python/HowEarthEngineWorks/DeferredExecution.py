import ee

image = ee.Image('CGIAR/SRTM90_V4')
operation = image.add(10)
# print(operation.getInfo())
print(operation)
