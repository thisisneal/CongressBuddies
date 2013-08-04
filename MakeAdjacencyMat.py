import os
import json
import yaml

pathToVoteDirs = "votes/2013/"
prefix = "h"

adjacenyMap = {} # Person onto {Person onto closeness count}
bioMap = {}  # ID onto bio data
nameMap = {} # Name onto ID

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

# Return GovTrack ID (used for profile pictures)
def getGovID(personID):
    return bioMap[personID][0]

# Return full name
def getName(personID):
    return bioMap[personID][1]

def getParty(personID):
    return bioMap[personID][3]

# Return votes ID from a full matched name
def getIDfromName(name):
    return nameMap[name.lower()]

# Get the top N buddies for a given person
def getBuddies(personID, num):
    try:
        friends = adjacenyMap[personID]
        sortedListTuples = sorted(friends.items(), key=lambda x: x[1], reverse=True)
        sortedNameList = []
        for curTuple in sortedListTuples:
            sortedNameList.append(curTuple[0])
        return sortedNameList[1:num+1]
    except:
        return []

# Populate bioMap
def getBios():
    global bioMap, nameMap
    BIO_FILE = prefix + "_BIO_MAP.json" # different serialization for house/senate
    # Pull congress bios from disk if possible
    if os.path.isfile(BIO_FILE):
        json_data = open(BIO_FILE).read()
        bioMap = json.loads(json_data)
    # Otherwise serialize the mapping after computing it
    else:
        pdata = yaml.load(open('legislators-current.yaml'))
        for person in pdata:
            try:
                if prefix == 'h':
                    keyID = person['id']['bioguide'] # ID used in house votes
                elif prefix == 's':
                    keyID = person['id']['lis'] # ID used in senate votes
                bioMap[keyID] =(person['id']['govtrack'],
                                person['name']['official_full'],
                                person['terms'][-1]['state'],
                                person['terms'][-1]['party'])
            except:
                pass
        fp = open(BIO_FILE, 'wb')
        json.dump(bioMap, fp)
    nameMap = {(v[1].lower()):k for k, v in bioMap.items()}

# Prepare lookup maps
def init():
    global adjacenyMap
    print "initializing backend..."
    getBios()
    MAP_FILE = prefix + "_ADJ_MAP.json"
    # Pull adjacency mapping from disk if possible
    if os.path.isfile(MAP_FILE):
        json_data = open(MAP_FILE).read()
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
        fp = open(MAP_FILE, 'wb')
        json.dump(adjacenyMap, fp)
    print "Done initializing backend."
    # Ad hoc:
    #buddies = getBuddies("P000523", 5)
    #for bro in buddies:
    #    print bro[0] + " : " + bioMap[bro[0]][1]