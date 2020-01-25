import ee 
from ee_plugin import Map 

dataset = ee.Image('CSP/ERGo/1_0/US/lithology')
lithology = dataset.select('b1')
lithologyVis = {
  'min': 0.0,
  'max': 20.0,
  'palette': [
    '356EFF', 'ACB6DA', 'D6B879', '313131', 'EDA800', '616161', 'D6D6D6',
    'D0DDAE', 'B8D279', 'D5D378', '141414', '6DB155', '9B6D55', 'FEEEC9',
    'D6B879', '00B7EC', 'FFDA90', 'F8B28C'
  ],
}
Map.setCenter(-105.8636, 40.3439, 11)
Map.addLayer(lithology, lithologyVis, 'Lithology')
