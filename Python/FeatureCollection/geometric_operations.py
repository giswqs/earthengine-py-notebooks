import ee 
from ee_plugin import Map 

# Create two circular geometries.
poly1 = ee.Geometry.Point([-50, 30]).buffer(1e6)
poly2 = ee.Geometry.Point([-40, 30]).buffer(1e6)

# Display polygon 1 in red and polygon 2 in blue.
Map.setCenter(-45, 30)
Map.addLayer(poly1, {'color': 'FF0000'}, 'poly1')
Map.addLayer(poly2, {'color': '0000FF'}, 'poly2')

# Compute the intersection, display it in blue.
intersection = poly1.intersection(poly2, ee.ErrorMargin(1))
Map.addLayer(intersection, {'color': '00FF00'}, 'intersection')

# Compute the union, display it in magenta.
union = poly1.union(poly2, ee.ErrorMargin(1))
Map.addLayer(union, {'color': 'FF00FF'}, 'union')

# Compute the difference, display in yellow.
diff1 = poly1.difference(poly2, ee.ErrorMargin(1))
Map.addLayer(diff1, {'color': 'FFFF00'}, 'diff1')

# Compute symmetric difference, display in black.
symDiff = poly1.symmetricDifference(poly2, ee.ErrorMargin(1))
Map.addLayer(symDiff, {'color': '000000'}, 'symmetric difference')

