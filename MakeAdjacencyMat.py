import os
import json

pathToVoteDirs = "votes/2013/"

def fooFile(jsonFile):
    json_data=open(jsonFile).read()
    data = json.loads(json_data)
    print(data)

for dirname, dirnames, filenames in os.walk(pathToVoteDirs):
    for subdirname in dirnames:
        fooFile(pathToVoteDirs + subdirname + "/data.json")
