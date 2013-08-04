import os
import json
import json

pathToVoteDirs = "votes/2013/"
prefix = "h"

adjacenyMap = {}
bioMap = {}

# Populate bioMap
def getBios():
    pass

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

# Get the top N buddies for a given person
def getBuddies(personID, num):
    friends = adjacenyMap[personID]
    sortedList = sorted(friends.items(), key=lambda x: x[1], reverse=True)
    return sortedList[:num]

def main():
    global adjacenyMap
    # Pull adjacency mapping from disk if possible
    if os.path.isfile("ADJ_MAP.json"):
        json_data = open('ADJ_MAP.json').read()
        adjacenyMap = json.loads(json_data)
    # Otherwise serialize the mapping after computing it
    else:
        for dirname, dirnames, filenames in os.walk(pathToVoteDirs):
            for subdirname in dirnames:
                if subdirname.startswith(prefix):
                    success = parseFile(pathToVoteDirs + subdirname + "/data.json")
                    if success :
                        print ". Parsed file for " + subdirname
                    else:
                        print "X Failed to parse file " + subdirname
        fp = open('ADJ_MAP.json', 'wb')
        json.dump(adjacenyMap, fp)
    #print json.dumps(adjacenyMap)
    #print adjacenyMap.keys()
    print getBuddies("K000378", 10)

main()