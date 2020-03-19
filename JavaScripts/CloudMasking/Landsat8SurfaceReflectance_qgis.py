import ee 
from ee_plugin import Map 

# This example demonstrates the use of the pixel QA band to mask
# clouds in surface reflectance (SR) data.  It is suitable
# for use with any of the Landsat SR datasets.

# Function to cloud mask from the pixel_qa band of Landsat 8 SR data.
def maskL8sr(image):
  # Bits 3 and 5 are cloud shadow and cloud, respectively.
  cloudShadowBitMask = 1 << 3
  cloudsBitMask = 1 << 5

  # Get the pixel QA band.
  qa = image.select('pixel_qa')

  # Both flags should be set to zero, indicating clear conditions.
  mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0) \
      .And(qa.bitwiseAnd(cloudsBitMask).eq(0))

  # Return the masked image, scaled to reflectance, without the QA bands.
  return image.updateMask(mask).divide(10000) \
      .select("B[0-9]*") \
      .copyProperties(image, ["system:time_start"])


# Map the function over one year of data.
collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR') \
    .filterDate('2016-01-01', '2016-12-31') \
    .map(maskL8sr)

composite = collection.median()

# Display the results.
Map.addLayer(composite, {'bands': ['B4',  'B3',  'B2'], 'min': 0, 'max': 0.3})
