# %%
"""
<table class="ee-notebook-buttons" align="left">
    <td><a target="_blank"  href="https://github.com/giswqs/earthengine-py-notebooks/tree/master/JavaScripts/Demos/Classification.ipynb"><img width=32px src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" /> View source on GitHub</a></td>
    <td><a target="_blank"  href="https://nbviewer.jupyter.org/github/giswqs/earthengine-py-notebooks/blob/master/JavaScripts/Demos/Classification.ipynb"><img width=26px src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/883px-Jupyter_logo.svg.png" />Notebook Viewer</a></td>
    <td><a target="_blank"  href="https://colab.research.google.com/github/giswqs/earthengine-py-notebooks/blob/master/JavaScripts/Demos/Classification.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" /> Run in Google Colab</a></td>
</table>
"""

# %%
"""
## Install Earth Engine API and geemap
Install the [Earth Engine Python API](https://developers.google.com/earth-engine/python_install) and [geemap](https://github.com/giswqs/geemap). The **geemap** Python package is built upon the [ipyleaflet](https://github.com/jupyter-widgets/ipyleaflet) and [folium](https://github.com/python-visualization/folium) packages and implements several methods for interacting with Earth Engine data layers, such as `Map.addLayer()`, `Map.setCenter()`, and `Map.centerObject()`.
The following script checks if the geemap package has been installed. If not, it will install geemap, which automatically installs its [dependencies](https://github.com/giswqs/geemap#dependencies), including earthengine-api, folium, and ipyleaflet.

**Important note**: A key difference between folium and ipyleaflet is that ipyleaflet is built upon ipywidgets and allows bidirectional communication between the front-end and the backend enabling the use of the map to capture user input, while folium is meant for displaying static data only ([source](https://blog.jupyter.org/interactive-gis-in-jupyter-with-ipyleaflet-52f9657fa7a)). Note that [Google Colab](https://colab.research.google.com/) currently does not support ipyleaflet ([source](https://github.com/googlecolab/colabtools/issues/60#issuecomment-596225619)). Therefore, if you are using geemap with Google Colab, you should use [`import geemap.eefolium`](https://github.com/giswqs/geemap/blob/master/geemap/eefolium.py). If you are using geemap with [binder](https://mybinder.org/) or a local Jupyter notebook server, you can use [`import geemap`](https://github.com/giswqs/geemap/blob/master/geemap/geemap.py), which provides more functionalities for capturing user input (e.g., mouse-clicking and moving).
"""

# %%
# Installs geemap package
import subprocess

try:
    import geemap
except ImportError:
    print('geemap package not installed. Installing ...')
    subprocess.check_call(["python", '-m', 'pip', 'install', 'geemap'])

# Checks whether this notebook is running on Google Colab
try:
    import google.colab
    import geemap.eefolium as geemap
except:
    import geemap

# Authenticates and initializes Earth Engine
import ee

try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize()  

# %%
"""
## Create an interactive map 
The default basemap is `Google MapS`. [Additional basemaps](https://github.com/giswqs/geemap/blob/master/geemap/basemaps.py) can be added using the `Map.add_basemap()` function. 
"""

# %%
Map = geemap.Map(center=[40,-100], zoom=4)
Map

# %%
"""
## Add Earth Engine Python script 
"""

# %%
# Add Earth Engine dataset
# This demonstration uses hand-located points to train a classifier.
# Each training point has a field called 'landcover' containing
# class labels at that location. The following block contains
# construction code for the points.  Hover on the 'urban' variable
# and click, 'Convert' in the dialog.
urban = ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([-122.40898132324219, 37.78247386188714]),
            {
              "landcover": 0,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.40623474121094, 37.77107659627034]),
            {
              "landcover": 0,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.39799499511719, 37.785187237567705]),
            {
              "landcover": 0,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.39936828613281, 37.772162125840445]),
            {
              "landcover": 0,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.41104125976562, 37.76890548932033]),
            {
              "landcover": 0,
              "system:index": "4"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.41859436035156, 37.7835592241132]),
            {
              "landcover": 0,
              "system:index": "5"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.41790771484375, 37.801465399617314]),
            {
              "landcover": 0,
              "system:index": "6"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.40142822265625, 37.77053382550901]),
            {
              "landcover": 0,
              "system:index": "7"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.39662170410156, 37.75370595587201]),
            {
              "landcover": 0,
              "system:index": "8"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.28950500488281, 37.8166551148543]),
            {
              "landcover": 0,
              "system:index": "9"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.28195190429688, 37.82696064199382]),
            {
              "landcover": 0,
              "system:index": "10"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.28126525878906, 37.81882481909333]),
            {
              "landcover": 0,
              "system:index": "11"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.2723388671875, 37.82858769894982]),
            {
              "landcover": 0,
              "system:index": "12"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.28607177734375, 37.84702517033112]),
            {
              "landcover": 0,
              "system:index": "13"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.29293823242188, 37.8562421777618]),
            {
              "landcover": 0,
              "system:index": "14"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.27302551269531, 37.849193981623955]),
            {
              "landcover": 0,
              "system:index": "15"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.28057861328125, 37.86545803289311]),
            {
              "landcover": 0,
              "system:index": "16"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.27096557617188, 37.820452055421086]),
            {
              "landcover": 0,
              "system:index": "17"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.27920532226562, 37.808518155993234]),
            {
              "landcover": 0,
              "system:index": "18"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.27783203125, 37.80092285199884]),
            {
              "landcover": 0,
              "system:index": "19"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.31491088867188, 37.784644570400836]),
            {
              "landcover": 0,
              "system:index": "20"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.31903076171875, 37.7835592241132]),
            {
              "landcover": 0,
              "system:index": "21"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.26959228515625, 37.80200794325057]),
            {
              "landcover": 0,
              "system:index": "22"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.40966796875, 37.768362702622596]),
            {
              "landcover": 0,
              "system:index": "23"
            })]),
vegetation = ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([-122.15835571289062, 37.81990964729775]),
            {
              "landcover": 1,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.14462280273438, 37.806890656610484]),
            {
              "landcover": 1,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.16522216796875, 37.817197546892785]),
            {
              "landcover": 1,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.09793090820312, 37.80797566018445]),
            {
              "landcover": 1,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.08282470703125, 37.81123057525427]),
            {
              "landcover": 1,
              "system:index": "4"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.07733154296875, 37.7992951852321]),
            {
              "landcover": 1,
              "system:index": "5"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.05398559570312, 37.77867496858311]),
            {
              "landcover": 1,
              "system:index": "6"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.05398559570312, 37.76673431862507]),
            {
              "landcover": 1,
              "system:index": "7"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.07389831542969, 37.792784159505125]),
            {
              "landcover": 1,
              "system:index": "8"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.0306396484375, 37.83455326751277]),
            {
              "landcover": 1,
              "system:index": "9"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.06497192382812, 37.831299380818606]),
            {
              "landcover": 1,
              "system:index": "10"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.19268798828125, 37.85461573076714]),
            {
              "landcover": 1,
              "system:index": "11"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.18170166015625, 37.849193981623955]),
            {
              "landcover": 1,
              "system:index": "12"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.51609802246094, 37.84051835371829]),
            {
              "landcover": 1,
              "system:index": "13"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.49137878417969, 37.838349287273296]),
            {
              "landcover": 1,
              "system:index": "14"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.50511169433594, 37.82641828170282]),
            {
              "landcover": 1,
              "system:index": "15"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.54081726074219, 37.84160286302103]),
            {
              "landcover": 1,
              "system:index": "16"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.55592346191406, 37.85353141283498]),
            {
              "landcover": 1,
              "system:index": "17"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.56278991699219, 37.86274760688767]),
            {
              "landcover": 1,
              "system:index": "18"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.54631042480469, 37.86328970006369]),
            {
              "landcover": 1,
              "system:index": "19"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.52708435058594, 37.85190490603355]),
            {
              "landcover": 1,
              "system:index": "20"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.52845764160156, 37.83889155986444]),
            {
              "landcover": 1,
              "system:index": "21"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.51472473144531, 37.83021472002989]),
            {
              "landcover": 1,
              "system:index": "22"
            })]),
water = ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([-122.61085510253906, 37.835095568009415]),
            {
              "landcover": 2,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.60673522949219, 37.8166551148543]),
            {
              "landcover": 2,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.60810852050781, 37.80038030039511]),
            {
              "landcover": 2,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.57102966308594, 37.80472060163741]),
            {
              "landcover": 2,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.58888244628906, 37.83455326751277]),
            {
              "landcover": 2,
              "system:index": "4"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.65205383300781, 37.855157883752504]),
            {
              "landcover": 2,
              "system:index": "5"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.62870788574219, 37.823164036248635]),
            {
              "landcover": 2,
              "system:index": "6"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.62664794921875, 37.792784159505125]),
            {
              "landcover": 2,
              "system:index": "7"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.60055541992188, 37.792784159505125]),
            {
              "landcover": 2,
              "system:index": "8"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.53738403320312, 37.7992951852321]),
            {
              "landcover": 2,
              "system:index": "9"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.57240295410156, 37.82641828170282]),
            {
              "landcover": 2,
              "system:index": "10"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.58682250976562, 37.823164036248635]),
            {
              "landcover": 2,
              "system:index": "11"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.36709594726562, 37.85570003275074]),
            {
              "landcover": 2,
              "system:index": "12"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.40074157714844, 37.88171849539308]),
            {
              "landcover": 2,
              "system:index": "13"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.40005493164062, 37.86925246182428]),
            {
              "landcover": 2,
              "system:index": "14"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.37739562988281, 37.88117653780091]),
            {
              "landcover": 2,
              "system:index": "15"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.34992980957031, 37.87358871277159]),
            {
              "landcover": 2,
              "system:index": "16"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.34992980957031, 37.85244707895444]),
            {
              "landcover": 2,
              "system:index": "17"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.34855651855469, 37.838349287273296]),
            {
              "landcover": 2,
              "system:index": "18"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.39387512207031, 37.849193981623955]),
            {
              "landcover": 2,
              "system:index": "19"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.44743347167969, 37.82262164805511]),
            {
              "landcover": 2,
              "system:index": "20"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.43850708007812, 37.842687356377084]),
            {
              "landcover": 2,
              "system:index": "21"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.354736328125, 37.789528431453014]),
            {
              "landcover": 2,
              "system:index": "22"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.25826263427734, 37.68952589794135]),
            {
              "landcover": 2,
              "system:index": "23"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.53326416015625, 37.81114015184751]),
            {
              "landcover": 2,
              "system:index": "24"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.44503021240234, 37.87078823552829]),
            {
              "landcover": 2,
              "system:index": "25"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.4532699584961, 37.86048883137166]),
            {
              "landcover": 2,
              "system:index": "26"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.33036041259766, 37.833920567528345]),
            {
              "landcover": 2,
              "system:index": "27"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.19989776611328, 37.65664491891396]),
            {
              "landcover": 2,
              "system:index": "28"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.21946716308594, 37.62374937200642]),
            {
              "landcover": 2,
              "system:index": "29"
            }),
        ee.Feature(
            ee.Geometry.Point([-122.24040985107422, 37.61504728801728]),
            {
              "landcover": 2,
              "system:index": "30"
            })])

# Load the Landsat 8 scaled radiance image collection.
landsatCollection = ee.ImageCollection('LANDSAT/LC08/C01/T1') \
    .filterDate('2017-01-01', '2017-12-31')

# Make a cloud-free composite.
composite = ee.Algorithms.Landsat.simpleComposite({
  'collection': landsatCollection,
  'asFloat': True
})

# Merge the three geometry layers into a single FeatureCollection.
newfc = urban.merge(vegetation).merge(water)

# Use these bands for classification.
bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7']
# The name of the property on the points storing the class label.
classProperty = 'landcover'

# Sample the composite to generate training data.  Note that the
# class label is stored in the 'landcover' property.
training = composite.select(bands).sampleRegions({
  'collection': newfc,
  'properties': [classProperty],
  'scale': 30
})

# Train a CART classifier.
classifier = ee.Classifier.smileCart().train({
  'features': training,
  'classProperty': classProperty,
})
# Print some info about the classifier (specific to CART).
print('CART, explained', classifier.explain())

# Classify the composite.
classified = composite.classify(classifier)
Map.centerObject(newfc)
Map.addLayer(classified, {'min': 0, 'max': 2, 'palette': ['red', 'green', 'blue']})

# Optionally, do some accuracy assessment.  Fist, add a column of
# random uniforms to the training dataset.
withRandom = training.randomColumn('random')

# We want to reserve some of the data for testing, to avoid overfitting the model.
split = 0.7;  # Roughly 70% training, 30% testing.
trainingPartition = withRandom.filter(ee.Filter.lt('random', split))
testingPartition = withRandom.filter(ee.Filter.gte('random', split))

# Trained with 70% of our data.
trainedClassifier = ee.Classifier.smileRandomForest(5).train({
  'features': trainingPartition,
  'classProperty': classProperty,
  'inputProperties': bands
})

# Classify the test FeatureCollection.
test = testingPartition.classify(trainedClassifier)

# Print the confusion matrix.
confusionMatrix = test.errorMatrix(classProperty, 'classification')
print('Confusion Matrix', confusionMatrix)


# %%
"""
## Display Earth Engine data layers 
"""

# %%
Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map