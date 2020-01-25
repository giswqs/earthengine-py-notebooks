import ee
from ee_plugin import Map

# Load a Landsat 8 raw image.
image = ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318')

# Define a RasterSymbolizer element with '_enhance_' for a placeholder.
template_sld = \
  '<RasterSymbolizer>' + \
    '<ContrastEnhancement><_enhance_/></ContrastEnhancement>' + \
    '<ChannelSelection>' + \
      '<RedChannel>' + \
        '<SourceChannelName>B5</SourceChannelName>' + \
      '</RedChannel>' + \
      '<GreenChannel>' + \
        '<SourceChannelName>B4</SourceChannelName>' + \
      '</GreenChannel>' + \
      '<BlueChannel>' + \
        '<SourceChannelName>B3</SourceChannelName>' + \
      '</BlueChannel>' + \
    '</ChannelSelection>' + \
  '</RasterSymbolizer>'

# Get SLDs with different enhancements.
equalize_sld = template_sld.replace('_enhance_', 'Histogram')
normalize_sld = template_sld.replace('_enhance_', 'Normalize')

# Display the results.
Map.centerObject(image, 10)
Map.addLayer(image, {'bands': ['B5', 'B4', 'B3'], 'min': 0, 'max': 15000}, 'Linear')
Map.addLayer(image.sldStyle(equalize_sld), {}, 'Equalized')
Map.addLayer(image.sldStyle(normalize_sld), {}, 'Normalized')