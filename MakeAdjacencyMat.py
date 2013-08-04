import os
import json

pathToVoteDirs = "votes/2013/"
prefix = "h"

# Increment the similarity count between two people
def incrementSimilarity(perA, perB):
    pass

# Given an array of individual votes that matched vote type and bill,
# increment the similarity counts in adjaceny matrix between all people involved
def countSamevotes(votes):
    for vote in votes:
        cur_person = vote['id']
        for vote in votes:
            other_person = vote['id']
        incrementSimilarity(cur_person, other_person)

def fooFile(jsonFile):
    json_data = open(jsonFile).read()
    data = json.loads(json_data)
    try:
        votes = data['votes']
        pres = votes['Present']
        ayes = votes['Yea']
        nays = votes['Nay']
        countSameVotes(ayes)
        countSameVotes(nays)
    except:
        pass

for dirname, dirnames, filenames in os.walk(pathToVoteDirs):
    for subdirname in dirnames:
        if subdirname.startswith(prefix):
            fooFile(pathToVoteDirs + subdirname + "/data.json")
