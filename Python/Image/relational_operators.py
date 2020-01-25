import ee 
from ee_plugin import Map 

# Load a 2012 nightlights image.
nl2012 = ee.Image('NOAA/DMSP-OLS/NIGHTTIME_LIGHTS/F182012')
lights = nl2012.select('stable_lights')

# Define arbitrary thresholds on the 6-bit stable lights band.
zones = lights.gt(30).add(lights.gt(55)).add(lights.gt(62))

# Display the thresholded image as three distinct zones near Paris.
palette = ['000000', '0000FF', '00FF00', 'FF0000']
Map.setCenter(2.373, 48.8683, 8)
Map.addLayer(zones, {'min': 0, 'max': 3, 'palette': palette}, 'development zones')

# Create zones using an expression, display.
zonesExp = nl2012.expression(
    "(b('stable_lights') > 62) ? 3" +
      ": (b('stable_lights') > 55) ? 2" +
        ": (b('stable_lights') > 30) ? 1" +
          ": 0"
)
Map.addLayer(zonesExp,
             {'min': 0, 'max': 3, 'palette': palette},
             'development zones (ternary)')

