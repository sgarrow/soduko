import pprint        as pp
import printRoutines as pr
#############################################################################

def pruneNakedTriples(canidates):
    from itertools import combinations

    print('\nPruning triplets')
    sqrDups123 = []
    squareNums = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]] 

    for squareNum in squareNums:
        rowsInSq = [ x+squareNum[0]*3 for x in [0,1,2] ]
        colsInSq = [ x+squareNum[1]*3 for x in [0,1,2] ]

        coordsInSq     = [ [r,c] for r in rowsInSq for c in colsInSq ]
        candatesSq     = [ canidates[x[0]][x[1]] for x in coordsInSq ] 
        candatesLen123 = [ x for x in candatesSq if x != 0 and len(x) in [2,3]]
        sqrDups123.append(candatesLen123)

    myDict = {}
    for idx,s in enumerate(sqrDups123):
        myDict[idx] = []
        comb = combinations(range(len(s)), 3)
        for i in comb:
            mySet = set( s[i[0]] + s[i[1]] + s[i[2]] )
            if len(mySet) == 3:
                #print(idx, mySet)
                myDict[idx].append(list(mySet))

    #pr.prettyPrint3DArray(canidates)
    pp.pprint(myDict)
    numPruned = 0
    for k in myDict:
        rowsInSq = [ x+squareNums[k][0]*3 for x in [0,1,2] ]
        colsInSq = [ x+squareNums[k][1]*3 for x in [0,1,2] ]

        for r in rowsInSq:
            for c in colsInSq:
                try:
                    intersection = set.intersection(set(canidates[r][c]), set(myDict[k][0])) # [0] means assuming only 1 naked triplet exists in theis square
                    valsOtherThanTriplet = set(canidates[r][c]) - intersection
                    #print('IIIIIIII', r, c, intersection, valsOtherThanTriplet)
                    if len(valsOtherThanTriplet) > 0:
                        for valToRemove in myDict[k][0]:
                            print('  Attempting to remove {} from {},{}'.format(valToRemove,r,c))
                            try:
                                canidates[r][c].remove(valToRemove)
                                numPruned += 1
                            except:
                                pass
                except:
                    pass
    print()

    print('  numPruned = {}.\n'.format(numPruned))
    pr.prettyPrint3DArray(canidates)
    return(numPruned, canidates)
#############################################################################

