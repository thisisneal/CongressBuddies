import os
import json

pathToVoteDirs = "votes/2013/"
prefix = "h"

def fooFile(jsonFile):
    json_data = open(jsonFile).read()
    data = json.loads(json_data)
    try:
        votes = data['votes']
        pres = votes['Present']
        ayes = votes['Yea']
        nays = votes['Nay']
        print json.dumps(ayes)
    except:
        pass

for dirname, dirnames, filenames in os.walk(pathToVoteDirs):
    for subdirname in dirnames:
        if subdirname.startswith(prefix):
            fooFile(pathToVoteDirs + subdirname + "/data.json")
