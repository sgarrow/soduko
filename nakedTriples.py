import pprint as pp
from itertools import combinations
#############################################################################

def printNakedTripletsDict(nakedTripleDict, Srq_Row_Col ):
    if nakedTripleDict == {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}:
        print( '    No {} naked triplets found'.format(Srq_Row_Col)) 
    else:
        for k,v in nakedTripleDict.items():
            if v != []:
                print('    {} {} has naked triple {}'.\
                      format(Srq_Row_Col, k, nakedTripleDict[k]))
#############################################################################

def buildRowNkdTripD(canidates):
    rowTriple23 = []

    for row in canidates:
        candatesLen23 = [ x for x in row if x != 0 and len(x) in [2,3]]
        rowTriple23.append(candatesLen23)

    rowNkdTripD = {}
    for idx,s in enumerate(rowTriple23):
        rowNkdTripD[idx] = []
        comb = combinations(range(len(s)), 3)
        for i in comb:
            mySet = set( s[i[0]] + s[i[1]] + s[i[2]] )
            if len(mySet) == 3:
                #print(idx, mySet)
                rowNkdTripD[idx].append(list(mySet))
    return rowNkdTripD
#############################################################################

def buildColNkdTripD(canidates):
    colTriple23 = []
    Xpos = [[row[i] for row in canidates] for i in range(len(canidates[0]))]

    for col in Xpos:
        candatesLen23 = [ x for x in col if x != 0 and len(x) in [2,3]]
        colTriple23.append(candatesLen23)

    colNkdTripD = {}
    for idx,s in enumerate(colTriple23):
        colNkdTripD[idx] = []
        comb = combinations(range(len(s)), 3)
        for i in comb:
            mySet = set( s[i[0]] + s[i[1]] + s[i[2]] )
            if len(mySet) == 3:
                #print(idx, mySet)
                colNkdTripD[idx].append(list(mySet))
    return colNkdTripD
#############################################################################

def buildSqrNkdTripD(canidates):
    sqrDups23 = []
    squareNums = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]] 

    for squareNum in squareNums:
        rowsInSq = [ x+squareNum[0]*3 for x in [0,1,2] ]
        colsInSq = [ x+squareNum[1]*3 for x in [0,1,2] ]

        coordsInSq   = [ [r,c] for r in rowsInSq for c in colsInSq ]
        candatesSq   = [ canidates[x[0]][x[1]] for x in coordsInSq ] 
        candatesLen23= [ x for x in candatesSq if x != 0 and len(x) in [2,3]]
        sqrDups23.append(candatesLen23)

    sqrNkdTripD = {}
    for idx,s in enumerate(sqrDups23):
        sqrNkdTripD[idx] = []
        comb = combinations(range(len(s)), 3)
        for i in comb:
            mySet = set( s[i[0]] + s[i[1]] + s[i[2]] )
            if len(mySet) == 3:
                #print(idx, mySet)
                sqrNkdTripD[idx].append(list(mySet))
    return sqrNkdTripD
#############################################################################

def pruneNakedTriplesRows(canidates):
    numPruned = 0
    print('  Finding naked triplets in rows')
    rowNkdTripD = buildRowNkdTripD(canidates)
    printNakedTripletsDict(rowNkdTripD, 'Row')
    if rowNkdTripD != {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}:
        print('  Pruning naked triplets in rows')
        #pr.prettyPrint3DArray(canidates)
        for rIdx,row in enumerate(canidates): # rIdx will be index into dict as
            for cIdx,el in enumerate(row):    # well as the canidates row number 
                try:
                    intersection = \
                    set.intersection(set(el),  # [0] means assuming only 1 naked
                    set(rowNkdTripD[rIdx][0])) # triplet exists in this sqr  
                    valsOtherThanTriplet = set(el) - intersection                       
                    #print('rIdx, cIdx, intersection, valsOtherThanTriplet)             
                    if len(valsOtherThanTriplet) > 0:
                        for valToRemove in rowNkdTripD[rIdx][0]:
                            try:
                                canidates[rIdx][cIdx].remove(valToRemove)
                                print('    Removed {} from {},{}'.\
                                      format(valToRemove,rIdx,cIdx))
                                numPruned += 1
                            except:
                                pass
                except:
                    pass

        print('  numPruned = {}.\n'.format(numPruned))
        #pr.prettyPrint3DArray(canidates)
    return(numPruned, canidates)
#############################################################################

def pruneNakedTriplesCols(canidates):
    numPruned = 0
    print('  Finding naked triplets in cols')
    colNkdTripD = buildColNkdTripD(canidates)
    printNakedTripletsDict(colNkdTripD, 'Col')
    if colNkdTripD != {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}:
        print('  Pruning naked triplets in cols')
        for rIdx,row in enumerate(canidates): 
            for cIdx,el in enumerate(row): # cIdx will be index into dict 
                try:                       # as well as the canidates col number                                     
                    intersection = \
                    set.intersection(set(el),  # [0] means assuming only 1 naked
                    set(colNkdTripD[cIdx][0])) # triplet exists in theis square  
                    valsOtherThanTriplet = set(el) - intersection
                    #print('rIdx, cIdx, intersection, valsOtherThanTriplet)
                    if len(valsOtherThanTriplet) > 0:
                        for valToRemove in colNkdTripD[cIdx][0]:
                            try:
                                canidates[rIdx][cIdx].remove(valToRemove)
                                print('    Removed {} from {},{}'.\
                                      format(valToRemove,rIdx,cIdx))
                                numPruned += 1
                            except:
                                pass
                except:
                    pass
    
        #pr.prettyPrint3DArray(canidates)
        print('  numPruned = {}.\n'.format(numPruned))
    return(numPruned, canidates)
#############################################################################

def pruneNakedTriplesSqrs(canidates):
    numPruned = 0
    print('  Finding naked triplets in squares')
    sqrNkdTripD = buildSqrNkdTripD(canidates)
    printNakedTripletsDict(sqrNkdTripD, 'Square')
    if sqrNkdTripD != {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}:
        print('  Pruning naked triplets in square')
        #pr.prettyPrint3DArray(canidates)
        squareNums = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]] 
        for k in sqrNkdTripD:
            rowsInSq = [ x+squareNums[k][0]*3 for x in [0,1,2] ]
            colsInSq = [ x+squareNums[k][1]*3 for x in [0,1,2] ]
    
            for r in rowsInSq:
                for c in colsInSq:
                    try:
                        intersection = \
                        set.intersection(set(canidates[r][c]), # [0] means assuming only 1 naked
                        set(sqrNkdTripD[k][0]))                # triplet exists in theis square  
                        valsOtherThanTriplet = set(canidates[r][c]) - intersection
                        #print('r, c, intersection, valsOtherThanTriplet)
                        if len(valsOtherThanTriplet) > 0:
                            for valToRemove in sqrNkdTripD[k][0]:
                                try:
                                    canidates[r][c].remove(valToRemove)
                                    print('    Removed {} from {},{}'.\
                                          format(valToRemove,r,c))
                                    numPruned += 1
                                except:
                                    pass
                    except:
                        pass
    
        print('  numPruned = {}.\n'.format(numPruned))
        #pr.prettyPrint3DArray(canidates)
    return(numPruned, canidates)
#############################################################################

def pruneNakedTriples(canidates):
    print('\nPruning naked triplets ********************************* Start')
    #pr.prettyPrint3DArray(canidates)
    numPruned = 0

    numPrunedRows, canidates = pruneNakedTriplesRows(canidates)
    numPrunedCols, canidates = pruneNakedTriplesCols(canidates)
    numPrunedSqrs, canidates = pruneNakedTriplesSqrs(canidates)

    numPruned =  numPrunedRows + numPrunedCols + numPrunedSqrs
    print('Pruning naked triplets *********************************** End')
    return(numPruned, canidates)
#############################################################################

