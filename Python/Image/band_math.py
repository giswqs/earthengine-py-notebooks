import ee 
from ee_plugin import Map 

# Load two 5-year Landsat 7 composites.
landsat1999 = ee.Image('LANDSAT/LE7_TOA_5YEAR/1999_2003')
landsat2008 = ee.Image('LANDSAT/LE7_TOA_5YEAR/2008_2012')

# Compute NDVI the hard way.
ndvi1999 = landsat1999.select('B4').subtract(landsat1999.select('B3')) \
               .divide(landsat1999.select('B4').add(landsat1999.select('B3')))

# Compute NDVI the easy way.
ndvi2008 = landsat2008.normalizedDifference(['B4', 'B3'])

# Compute the multi-band difference image.
diff = landsat2008.subtract(landsat1999)
Map.addLayer(diff,
             {'bands': ['B4', 'B3', 'B2'], 'min': -32, 'max': 32},
             'difference')

# Compute the squared difference in each band.
squaredDifference = diff.pow(2)
Map.addLayer(squaredDifference,
             {'bands': ['B4', 'B3', 'B2'], 'max': 1000},
             'squared diff.')

