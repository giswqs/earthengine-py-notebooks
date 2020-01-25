import os, ee, datetime, csv, time



startTime = datetime.datetime(2001, 1, 1)
endTime = datetime.datetime(2001, 2, 1)

lst = ee.ImageCollection('FORA0125_H002').filterDate(startTime, endTime)

# Get the time series at these points.
points = [ee.Geometry.Point(-85.16516, 30.850000000000001)]
collection = ee.FeatureCollection(points)


# Extract the values by running reduceRegions over each image in the image collection.
def myfunction(i):
    return i.reduceRegions(collection, 'first')


values = lst.map(myfunction).flatten()

# Turn the result into a feature collection and export it.
taskParams = {
    'driveFolder': 'image',
    'driveFileNamePrefix': 'TylerTest',
    'fileFormat': 'CSV'
}

MyTry = ee.batch.Export.table(values, 'lst_timeseries', taskParams)
MyTry.start()
state = MyTry.status()['state']
while state in ['READY', 'RUNNING']:
    print(state, '...')
    time.sleep(1)
    state = MyTry.status()['state']
print('Done.', MyTry.status())
