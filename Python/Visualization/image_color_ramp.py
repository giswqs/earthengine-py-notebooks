import ee
from ee_plugin import Map

# Load SRTM Digital Elevation Model data.
image = ee.Image('CGIAR/SRTM90_V4');

# Define an SLD style of discrete intervals to apply to the image.
sld_intervals = \
  '<RasterSymbolizer>' + \
    '<ColorMap  type="intervals" extended="false" >' + \
      '<ColorMapEntry color="#0000ff" quantity="0" label="0"/>' + \
      '<ColorMapEntry color="#00ff00" quantity="100" label="1-100" />' + \
      '<ColorMapEntry color="#007f30" quantity="200" label="110-200" />' + \
      '<ColorMapEntry color="#30b855" quantity="300" label="210-300" />' + \
      '<ColorMapEntry color="#ff0000" quantity="400" label="310-400" />' + \
      '<ColorMapEntry color="#ffff00" quantity="1000" label="410-1000" />' + \
    '</ColorMap>' + \
  '</RasterSymbolizer>';

# Define an sld style color ramp to apply to the image.
sld_ramp = \
  '<RasterSymbolizer>' + \
    '<ColorMap type="ramp" extended="false" >' + \
      '<ColorMapEntry color="#0000ff" quantity="0" label="0"/>' + \
      '<ColorMapEntry color="#00ff00" quantity="100" label="100" />' + \
      '<ColorMapEntry color="#007f30" quantity="200" label="200" />' + \
      '<ColorMapEntry color="#30b855" quantity="300" label="300" />' + \
      '<ColorMapEntry color="#ff0000" quantity="400" label="400" />' + \
      '<ColorMapEntry color="#ffff00" quantity="500" label="500" />' + \
    '</ColorMap>' + \
  '</RasterSymbolizer>';

# Add the image to the map using both the color ramp and interval schemes.
Map.setCenter(-76.8054, 42.0289, 8);
Map.addLayer(image.sldStyle(sld_intervals), {}, 'SLD intervals');
Map.addLayer(image.sldStyle(sld_ramp), {}, 'SLD ramp');