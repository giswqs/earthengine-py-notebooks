import ee


image = ee.Image('LANDSAT/LC8_L1T/LC80440342014077LGN00').select(0)
print('Projection, crs, and crs_transform:', image.projection().getInfo())
print('Scale in meters:', image.projection().nominalScale().getInfo())
