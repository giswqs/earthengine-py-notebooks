import ee
from ee_plugin import Map

cover = ee.Image('MODIS/051/MCD12Q1/2012_01_01').select('Land_Cover_Type_1')

# Define an SLD style of discrete intervals to apply to the image.
sld_intervals = \
'<RasterSymbolizer>' + \
 ' <ColorMap  type="intervals" extended="false" >' + \
    '<ColorMapEntry color="#aec3d4" quantity="0" label="Water"/>' + \
    '<ColorMapEntry color="#152106" quantity="1" label="Evergreen Needleleaf Forest"/>' + \
    '<ColorMapEntry color="#225129" quantity="2" label="Evergreen Broadleaf Forest"/>' + \
    '<ColorMapEntry color="#369b47" quantity="3" label="Deciduous Needleleaf Forest"/>' + \
    '<ColorMapEntry color="#30eb5b" quantity="4" label="Deciduous Broadleaf Forest"/>' + \
    '<ColorMapEntry color="#387242" quantity="5" label="Mixed Deciduous Forest"/>' + \
    '<ColorMapEntry color="#6a2325" quantity="6" label="Closed Shrubland"/>' + \
    '<ColorMapEntry color="#c3aa69" quantity="7" label="Open Shrubland"/>' + \
    '<ColorMapEntry color="#b76031" quantity="8" label="Woody Savanna"/>' + \
    '<ColorMapEntry color="#d9903d" quantity="9" label="Savanna"/>' + \
    '<ColorMapEntry color="#91af40" quantity="10" label="Grassland"/>' + \
    '<ColorMapEntry color="#111149" quantity="11" label="Permanent Wetland"/>' + \
    '<ColorMapEntry color="#cdb33b" quantity="12" label="Cropland"/>' + \
    '<ColorMapEntry color="#cc0013" quantity="13" label="Urban"/>' + \
    '<ColorMapEntry color="#33280d" quantity="14" label="Crop, Natural Veg. Mosaic"/>' + \
    '<ColorMapEntry color="#d7cdcc" quantity="15" label="Permanent Snow, Ice"/>' + \
    '<ColorMapEntry color="#f7e084" quantity="16" label="Barren, Desert"/>' + \
    '<ColorMapEntry color="#6f6f6f" quantity="17" label="Tundra"/>' + \
  '</ColorMap>' + \
'</RasterSymbolizer>'
Map.addLayer(cover.sldStyle(sld_intervals), {}, 'IGBP classification styled')