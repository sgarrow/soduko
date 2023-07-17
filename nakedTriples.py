import pprint        as pp
from itertools import combinations
#############################################################################

def printNakedTripletsDict(nakedTripleDict, Srq_Row_Col ):
    if nakedTripleDict == {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}:
        print( '    No {} naked triplets found'.format(Srq_Row_Col)) 
    else:
        for k,v in nakedTripleDict.items():
            if v != []:
                print('    {} {} has naked triple {}'.format(Srq_Row_Col, k, nakedTripleDict[k]))
#############################################################################

def buildSqrNakedTripleDict(canidates):
    sqrDups123 = []
    squareNums = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]] 

    for squareNum in squareNums:
        rowsInSq = [ x+squareNum[0]*3 for x in [0,1,2] ]
        colsInSq = [ x+squareNum[1]*3 for x in [0,1,2] ]

        coordsInSq     = [ [r,c] for r in rowsInSq for c in colsInSq ]
        candatesSq     = [ canidates[x[0]][x[1]] for x in coordsInSq ] 
        candatesLen123 = [ x for x in candatesSq if x != 0 and len(x) in [2,3]]
        sqrDups123.append(candatesLen123)

    sqrNakedTripleDict = {}
    for idx,s in enumerate(sqrDups123):
        sqrNakedTripleDict[idx] = []
        comb = combinations(range(len(s)), 3)
        for i in comb:
            mySet = set( s[i[0]] + s[i[1]] + s[i[2]] )
            if len(mySet) == 3:
                #print(idx, mySet)
                sqrNakedTripleDict[idx].append(list(mySet))
    return sqrNakedTripleDict
#############################################################################

def buildRowNakedTripleDict(canidates):
    rowTriple23 = []

    for row in canidates:
        candatesLen23 = [ x for x in row if x != 0 and len(x) in [2,3]]
        rowTriple23.append(candatesLen23)

    rowNakedTripleDict = {}
    for idx,s in enumerate(rowTriple23):
        rowNakedTripleDict[idx] = []
        comb = combinations(range(len(s)), 3)
        for i in comb:
            mySet = set( s[i[0]] + s[i[1]] + s[i[2]] )
            if len(mySet) == 3:
                #print(idx, mySet)
                rowNakedTripleDict[idx].append(list(mySet))
    return rowNakedTripleDict
#############################################################################

def buildColNakedTripleDict(canidates):
    colTriple23 = []
    Xpos = [[row[i] for row in canidates] for i in range(len(canidates[0]))]

    for col in Xpos:
        candatesLen23 = [ x for x in col if x != 0 and len(x) in [2,3]]
        colTriple23.append(candatesLen23)

    colNakedTripleDict = {}
    for idx,s in enumerate(colTriple23):
        colNakedTripleDict[idx] = []
        comb = combinations(range(len(s)), 3)
        for i in comb:
            mySet = set( s[i[0]] + s[i[1]] + s[i[2]] )
            if len(mySet) == 3:
                #print(idx, mySet)
                colNakedTripleDict[idx].append(list(mySet))
    return colNakedTripleDict
#############################################################################

def pruneNakedTriples(canidates):

    print('\nPruning naked triplets ********************************* Start')
    #pr.prettyPrint3DArray(canidates)
    numPruned = 0
    ####################################################################

    print('  Finding naked triplets in squares')
    sqrNakedTripleDict = buildSqrNakedTripleDict(canidates)
    printNakedTripletsDict(sqrNakedTripleDict, 'Square')
    if sqrNakedTripleDict != {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}:
        print('  Pruning naked triplets in square based on square naked triplets')
        #pr.prettyPrint3DArray(canidates)
        squareNums = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]] 
        for k in sqrNakedTripleDict:
            rowsInSq = [ x+squareNums[k][0]*3 for x in [0,1,2] ]
            colsInSq = [ x+squareNums[k][1]*3 for x in [0,1,2] ]
    
            for r in rowsInSq:
                for c in colsInSq:
                    try:
                        intersection = set.intersection(set(canidates[r][c]), set(sqrNakedTripleDict[k][0])) # [0] means assuming only 1 naked triplet exists in theis square
                        valsOtherThanTriplet = set(canidates[r][c]) - intersection
                        #print('IIIIIIII', r, c, intersection, valsOtherThanTriplet)
                        if len(valsOtherThanTriplet) > 0:
                            for valToRemove in sqrNakedTripleDict[k][0]:
                                try:
                                    canidates[r][c].remove(valToRemove)
                                    print('    Removed {} from {},{}'.format(valToRemove,r,c))
                                    numPruned += 1
                                except:
                                    pass
                    except:
                        pass
    
        print('  numPruned = {}.\n'.format(numPruned))
        #pr.prettyPrint3DArray(canidates)
    ####################################################################

    print('  Finding naked triplets in rows')
    rowNakedTripleDict = buildRowNakedTripleDict(canidates)
    printNakedTripletsDict(rowNakedTripleDict, 'Row')
    if rowNakedTripleDict != {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}:
        print('  Pruning naked triplets in rows based on row naked triplets')
        #pr.prettyPrint3DArray(canidates)
        for rIdx,row in enumerate(canidates): # rIdx will be index into dict as well as the canidates row number
            for cIdx,el in enumerate(row):
                try:
                    intersection = set.intersection(set(el), set(rowNakedTripleDict[rIdx][0])) # [0] means assuming only 1 naked triplet exists in theis square
                    valsOtherThanTriplet = set(el) - intersection
                    #print('IIIIIIII', rIdx, cIdx, intersection, valsOtherThanTriplet)
                    if len(valsOtherThanTriplet) > 0:
                        for valToRemove in rowNakedTripleDict[rIdx][0]:
                            try:
                                canidates[rIdx][cIdx].remove(valToRemove)
                                print('    Removed {} from {},{}'.format(valToRemove,rIdx,cIdx))
                                numPruned += 1
                            except:
                                pass
                except:
                    pass

        print('  numPruned = {}.\n'.format(numPruned))
        #pr.prettyPrint3DArray(canidates)
    ####################################################################

    print('  Finding naked triplets in cols')
    colNakedTripleDict = buildColNakedTripleDict(canidates)
    printNakedTripletsDict(colNakedTripleDict, 'Col')
    if colNakedTripleDict != {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}:
        print('  Pruning naked triplets in cols based on col naked triplets')
        for rIdx,row in enumerate(canidates): 
            for cIdx,el in enumerate(row):    # cIdx will be index into dict as well as the canidates col number 
                try:
                    intersection = set.intersection(set(el), set(colNakedTripleDict[cIdx][0])) # [0] means assuming only 1 naked triplet exists in theis square
                    valsOtherThanTriplet = set(el) - intersection
                    #print('IIIIIIII', rIdx, cIdx, intersection, valsOtherThanTriplet)
                    if len(valsOtherThanTriplet) > 0:
                        for valToRemove in colNakedTripleDict[cIdx][0]:
                            try:
                                canidates[rIdx][cIdx].remove(valToRemove)
                                print('    Removed {} from {},{}'.format(valToRemove,rIdx,cIdx))
                                numPruned += 1
                            except:
                                pass
                except:
                    pass
    
        #pr.prettyPrint3DArray(canidates)
        print('  numPruned = {}.\n'.format(numPruned))
    ####################################################################
    print('Pruning naked triplets *********************************** End')
    return(numPruned, canidates)
#############################################################################

