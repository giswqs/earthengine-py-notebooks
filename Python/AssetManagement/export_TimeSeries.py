# from IPython.display import Image
import ee



# define the geometry
geometry = ee.Geometry.Polygon([[116.49078369140625, 39.82219623803342],
                                [116.49456024169922, 39.763105626443306],
                                [116.57455444335938, 39.76336953661037],
                                [116.57421112060547, 39.8211414937017],
                                [116.49078369140625, 39.82219623803342]])
geometry = geometry.bounds()


# mask out cloud covered regions
def maskBadData(image):
    valid = image.select('cfmask').eq(0)
    clean = image.mask(valid)
    return clean


# get the image collection
LC8 = ee.ImageCollection("LANDSAT/LC8_SR")
LC8_clean = LC8.filterDate("2015-01-01", "2015-12-31").filterBounds(geometry).map(maskBadData)
# get image informaiton
count = LC8_clean.size().getInfo()
sceneList = LC8_clean.aggregate_array('system:index').getInfo()
print(count)
print(sceneList)

# Loop to output each image
for i in range(0, count):
    scenename = 'LANDSAT/LC8_SR/' + sceneList[i]
    valid = ee.Image(scenename).select('cfmask').lt(2).clip(geometry)

    meanStat = valid.reduceRegion(reducer=ee.Reducer.mean(), maxPixels=1e9).getInfo()
    print(scenename, meanStat)

    if meanStat['cfmask'] > 0:
        print(scenename, " is valid")
        layer = ee.Image(scenename).mask(valid).select(
            ['B2', 'B3', 'B4', 'B5', 'B6', 'B7'], ['B1', 'B2', 'B3', 'B4', 'B5', 'B7'])
        layerClip = layer.clip(geometry)
        # visualize
        # Image(url=layer.getThumbUrl())

        # export
        exportname = 'segID_0_' + sceneList[i]
        task = ee.batch.Export.image.toDrive(image=layerClip, description=exportname, scale=30)
        task.start()
        # ee.batch.Task.list()
    else:
        print(scenename, " is invalid")
# print(exportname)
