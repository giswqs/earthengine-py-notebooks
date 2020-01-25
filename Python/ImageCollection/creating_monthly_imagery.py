# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/ImageCollection/creating_monthly_imagery.py

import ee
from ee_plugin import Map

p1 = ee.Geometry.Point([103.521, 13.028])
p2 = ee.Geometry.Point([105.622, 13.050])
Date_Start = ee.Date('2000-05-01')
Date_End = ee.Date('2007-12-01')
Date_window = ee.Number(30)

# Create list of dates for time series
n_months = Date_End.difference(Date_Start, 'month').round()
print("Number of months:", n_months.getInfo())
dates = ee.List.sequence(0, n_months, 1)
print(dates.getInfo())

def make_datelist(n):
    return Date_Start.advance(n, 'month')


dates = dates.map(make_datelist)
print(dates.getInfo())


def fnc(d1):
    S1 = ee.ImageCollection('LANDSAT/LT5_L1T_TOA') \
        .filterDate('2000-05-01', '2007-12-01') \
        .filter(ee.Filter.calendarRange(1, 14, 'month')) \
        .sort('CLOUD_COVER') \
        .filterBounds(p1).first()
    S2 = ee.ImageCollection('LANDSAT/LT5_L1T_TOA') \
        .filterDate('2000-05-01', '2007-12-01') \
        .filter(ee.Filter.calendarRange(1, 14, 'month')) \
        .sort('CLOUD_COVER') \
        .filterBounds(p2).first()

    mosaic = ee.ImageCollection([ee.Image(S1), ee.Image(S2)]).mosaic()

    return mosaic


list_of_images = dates.map(fnc)
print('list_of_images', list_of_images.getInfo())
mt = ee.ImageCollection(list_of_images)
print(mt.getInfo())
# Map.addLayer(mt, {}, 'mt')
