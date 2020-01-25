import ee

serverString = ee.String('I am not a String!')
print(type(serverString))

clientString = 'I am a String'
print(type(clientString))

serverList = ee.List.sequence(0, 7)
print(serverList.getInfo())
serverList = serverList.map(lambda n: ee.Number(n).add(1))
print(serverList.getInfo())
