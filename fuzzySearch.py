def min(intA, intB):
    if(intA < intB): return intA
    return intB

def dist(strA, strB):
    lenA = len(strA)
    lenB = len(strA)

    if(len(strA) == 0): return lenB
    if(len(strB) == 0): return lenA

    cost = 0
    if (strA[lenA-1] != strB[lenB-1]): cost = 1;

    return min(min(dist(strA[0:lenA-1], strB)+1, dist(strA, strB[0:lenB-1])+1),
            dist(strA[0:lenA-1], strB[0:lenB-1])+cost)
