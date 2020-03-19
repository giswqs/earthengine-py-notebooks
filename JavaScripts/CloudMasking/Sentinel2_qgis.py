import ee 
from ee_plugin import Map 

# This example uses the Sentinel-2 QA band to cloud mask
# the collection.  The Sentinel-2 cloud flags are less
# selective, so the collection is also pre-filtered by the
# CLOUDY_PIXEL_PERCENTAGE flag, to use only relatively
# cloud-free granule.

# Function to mask clouds using the Sentinel-2 QA band.
def maskS2clouds(image):
  qa = image.select('QA60')

  # Bits 10 and 11 are clouds and cirrus, respectively.
  cloudBitMask = 1 << 10
  cirrusBitMask = 1 << 11

  # Both flags should be set to zero, indicating clear conditions.
  mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(
             qa.bitwiseAnd(cirrusBitMask).eq(0))

  # Return the masked and scaled data, without the QA bands.
  return image.updateMask(mask).divide(10000) \
      .select("B.*") \
      .copyProperties(image, ["system:time_start"])


# Map the function over one year of data and take the median.
# Load Sentinel-2 TOA reflectance data.
collection = ee.ImageCollection('COPERNICUS/S2') \
    .filterDate('2016-01-01', '2016-12-31') \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
    .map(maskS2clouds)

composite = collection.median()

# Display the results.
Map.addLayer(composite, {'bands': ['B4',  'B3',  'B2'], 'min': 0, 'max': 0.3}, 'RGB')
