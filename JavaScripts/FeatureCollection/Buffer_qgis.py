import ee 
from ee_plugin import Map 

# Feature buffer example.
# Display the area within 2 kilometers of San Francisco BART stations.

# Instantiate a FeatureCollection of BART locations in Downtown San Francisco
# (points).
stations = [
  ee.Feature(
      ee.Geometry.Point(-122.42, 37.77), {'name': '16th St. Mission (16TH)'}),
  ee.Feature(
      ee.Geometry.Point(-122.42, 37.75), {'name': '24th St. Mission (24TH)'}),
  ee.Feature(
      ee.Geometry.Point(-122.41, 37.78),
      {'name': 'Civic Center/UN Plaza (CIVC)'})
]
bartStations = ee.FeatureCollection(stations)

# Map a function over the collection to buffer each feature.

def func_dky(f):
  return f.buffer(2000, 100); # Note that the errorMargin is set to 100.

buffered = bartStations.map(func_dky)




Map.addLayer(buffered, {'color': '800080'})

Map.setCenter(-122.4, 37.7, 11)
