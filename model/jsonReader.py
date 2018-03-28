import json
#! /usr/bin/python

# https://stackoverflow.com/questions/7771011/parse-json-in-python This is where I got some of the logic. 

def Parse():
	
#cube='1'

	data = []
firstCollom = []
secondCollom =[]
biglist = []
json_file='testdata.json'

with open(json_file) as json_data:
		data = json.load(json_data)
		print(json.dumps(data, indent=4))

for key, value in data.iteritems():
		y = [key,value] 
		biglist.append(y)
newList=[item for item in biglist if isinstance(item,tuple)]
	#firstCollom.append(key)
    #secondCollom.append(value)
print(biglist)
#print(firstCollom)
#print(secondCollom)


for x in firstCollom:
	print(x)
for x in secondCollom:
	print(x)




##print(data["Spoken Word"])






