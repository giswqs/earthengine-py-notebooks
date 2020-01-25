import ee

image = ee.Image('LANDSAT/LC8_L1T/LC80440342014077LGN00')

bandNames = image.bandNames()
print('Band names: ', bandNames.getInfo()) # ee.List

b1proj = image.select('B1').projection()
print('Band 1 projection: ', b1proj.getInfo()) # ee.Projection

b1scale = image.select('B1').projection().nominalScale()
print('Band 1 scale: ', b1scale.getInfo()) # ee.Number

b8scale = image.select('B8').projection().nominalScale()
print('Band 8 scale: ', b8scale.getInfo()) # ee.Number

properties = image.propertyNames()
print('Metadata properties: ', properties.getInfo()) # ee.List

cloudiness = image.get('CLOUD_COVER')
print('CLOUD_COVER: ', cloudiness.getInfo()) # ee.Number

date = ee.Date(image.get('system:time_start'))
print('Timestamp: ', date.getInfo()) # ee.Date
