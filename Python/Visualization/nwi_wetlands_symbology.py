# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Visualization/nwi_wetlands_symbology.py

import ee
from ee_plugin import Map

# NWI legend: https://www.fws.gov/wetlands/Data/Mapper-Wetlands-Legend.html
def nwi_add_color(fc):
    emergent = ee.FeatureCollection(
        fc.filter(ee.Filter.eq('WETLAND_TY', 'Freshwater Emergent Wetland')))
    emergent = emergent.map(lambda f: f.set(
        'R', 127).set('G', 195).set('B', 28))
    # print(emergent.first())

    forested = fc.filter(ee.Filter.eq(
        'WETLAND_TY', 'Freshwater Forested/Shrub Wetland'))
    forested = forested.map(lambda f: f.set('R', 0).set('G', 136).set('B', 55))

    pond = fc.filter(ee.Filter.eq('WETLAND_TY', 'Freshwater Pond'))
    pond = pond.map(lambda f: f.set('R', 104).set('G', 140).set('B', 192))

    lake = fc.filter(ee.Filter.eq('WETLAND_TY', 'Lake'))
    lake = lake.map(lambda f: f.set('R', 19).set('G', 0).set('B', 124))

    riverine = fc.filter(ee.Filter.eq('WETLAND_TY', 'Riverine'))
    riverine = riverine.map(lambda f: f.set(
        'R', 1).set('G', 144).set('B', 191))

    fc = ee.FeatureCollection(emergent.merge(
        forested).merge(pond).merge(lake).merge(riverine))

    base = ee.Image(0).mask(0).toInt8()
    img = base.paint(fc, 'R') \
        .addBands(base.paint(fc, 'G')
                  .addBands(base.paint(fc, 'B')))
    return img


fromFT = ee.FeatureCollection("users/wqs/Pipestem/Pipestem_HUC10")
Map.addLayer(ee.Image().paint(fromFT, 0, 2), {}, 'Watershed')
huc8_id = '10160002'
nwi_asset_path = 'users/wqs/NWI-HU8/HU8_' + huc8_id + '_Wetlands'    # NWI wetlands for the clicked watershed
clicked_nwi_huc = ee.FeatureCollection(nwi_asset_path)
nwi_color = nwi_add_color(clicked_nwi_huc)
Map.centerObject(clicked_nwi_huc, 10)
Map.addLayer(nwi_color, {'gamma': 0.3, 'opacity': 0.7}, 'NWI Wetlands Color')
