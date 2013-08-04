import os
import json

pathToVoteDirs = "votes/2013/"
prefix = "h"

adjacenyMap = {}

# Increment the similarity count between two people
def incrementSimilarityBi(perA, perB):
    incrementSimilarity(perA, perB)
    incrementSimilarity(perB, perA)

def incrementSimilarity(perA, perB):
    if perA not in adjacenyMap:
        adjacenyMap[perA] = {}
    if perB not in adjacenyMap[perA]:
        adjacenyMap[perA][perB] = 0
    adjacenyMap[perA][perB] += 1

# Given an array of individual votes that matched vote type and bill,
# increment the similarity counts in adjaceny matrix between all people involved
def countSameVotes(votes):
    for vote in votes:
        cur_person = vote['id']
        for vote in votes:
            other_person = vote['id']
            incrementSimilarityBi(cur_person, other_person)

# Count the similarities within a given vote data json file
def parseFile(jsonFile):
    json_data = open(jsonFile).read()
    data = json.loads(json_data)
    try:
        votes = data['votes']
        #pres = votes['Present']
        ayes = votes['Yea']
        countSameVotes(ayes)
        nays = votes['Nay']
        countSameVotes(nays)
        return True
    except Exception, err:
        #print Exception, err
        return False

def main():
    for dirname, dirnames, filenames in os.walk(pathToVoteDirs):
        for subdirname in dirnames:
            if subdirname.startswith(prefix):
                success = parseFile(pathToVoteDirs + subdirname + "/data.json")
                if success :
                    print ". Parsed file for " + subdirname
                else:
                    print "X Failed to parse file " + subdirname
    print adjacenyMap

main()