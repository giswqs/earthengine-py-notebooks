import ee 
from ee_plugin import Map 

def getCols(tableMetadata):
    return tableMetadata.columns

# Import a protected areas point feature collection.
wdpa = ee.FeatureCollection("WCMC/WDPA/current/points")

# Define a function to print metadata column names and datatypes. This function
# is intended to be applied by the `evaluate` method which provides the
# function a client-side dictionary allowing the 'columns' object of the
# feature collection metadata to be subset by dot notation or bracket notation
# (`tableMetadata['columns']`).
# function getCols(tableMetadata) {
#   print(tableMetadata.columns)
# }

# Fetch collection metadata (`.limit(0)`) and apply the
# previously defined function using `evaluate()`. The printed object is a
# dictionary where keys are column names and values are datatypes.
# print(getCols(wdpa.limit(0)).getInfo())
