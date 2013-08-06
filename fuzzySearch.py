def min(intA, intB):
    if(intA < intB): return intA
    return intB

#Compute the Levenshtein distance between strings s and t
def dist(s, t):
    m = len(s)
    n = len(t)
    d = [[0 for i in xrange(n+1)] for j in range(m+1)]

    for i in xrange(1, m+1):
        d[i][0] = i

    for j in xrange(1, n+1):
        d[0][j] = j

    for j in xrange(1, n+1):
        for i in xrange(1, m+1):
            if s[i-1] == t[j-1]: d[i][j] = d[i-1][j-1]
            else: d[i][j] = min(min(d[i-1][j]+1, d[i][j-1]+1), d[i-1][j-1]+1)

    return d[m][n]
