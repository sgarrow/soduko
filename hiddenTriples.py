from itertools import combinations
import printRoutines as pr
import pprint as pp
import fillRoutines  as fr

def mapSrqsToRows(canidates): # In canidates rows are rows
    sqrsToRows = []
    squareNums = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]] 

    for squareNum in squareNums:
        rowsInSq = [ x+squareNum[0]*3 for x in [0,1,2] ]
        colsInSq = [ x+squareNum[1]*3 for x in [0,1,2] ]
        coordsInSq   = [ [r,c] for r in rowsInSq for c in colsInSq ]
        candatesSq   = [ canidates[x[0]][x[1]] for x in coordsInSq ] 
        sqrsToRows.append(candatesSq)
    return sqrsToRows
#############################################################################

def mapRowsToSqrs(canidates): # In canidates rows are squares
    rowsToSqrs = []
    squareNums = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]] 
    rowsToSqrs = [ [None]*9 for i in range(9) ]

    for ii,squareNum in enumerate(squareNums):
        currRowToMap = canidates[ii]
        rowsInSq = [ x+squareNum[0]*3 for x in [0,1,2] ]
        colsInSq = [ x+squareNum[1]*3 for x in [0,1,2] ]
    
        for ii,r in enumerate(rowsInSq):
            for jj,c in enumerate(colsInSq):
                rowsToSqrs[r][c] = currRowToMap[ii*3+jj]
    return rowsToSqrs
#############################################################################

def mapRowsToCols(canidates):
    Xpos = [[row[i] for row in canidates] for i in range(len(canidates[0]))]
    return Xpos
#############################################################################

def mapColsToRows(canidates):
    Xpos = [[row[i] for row in canidates] for i in range(len(canidates[0]))]
    return Xpos
#############################################################################

def pruneHiddenTriples(canidates, house):

    import copy
    if   house == 'row':  Xcanidates = copy.deepcopy(canidates)
    elif house == 'col':  Xcanidates = mapColsToRows(canidates) 
    elif house == 'sqr':  Xcanidates = mapSrqsToRows(canidates)

    numPruned = 0
    for idx, rowOrColOrSqrWithZeros in enumerate(Xcanidates):
        rowOrColOrSqr = [set(x) if x != 0 else set([0]) for x in rowOrColOrSqrWithZeros]
        combSet       = combinations(rowOrColOrSqr, 3)  # C(n,r) = n! / ( r! * (n-r)! ). C(9,3) = 84.
        combIdxs      = list((i,j,k) for ((i,_),(j,_),(k,_)) in combinations(enumerate(rowOrColOrSqr), 3))

        for comb,comIdx in zip(combSet,combIdxs):

            if any( el == {0} for el in comb): continue
            else:                              pass

            T   = comIdx
            Tc  = [ x for x in range(0,len(rowOrColOrSqr)) if x not in T ]
            H   = set.union( comb[0], comb[1], comb[2] )
            G   = set(fr.flatten([ rowOrColOrSqr[ii] for ii in Tc if rowOrColOrSqr[ii] != [0]]))
            HmG = list(H - G)
            hIsNaked  = (len(H) == 3)
            hIsHidden = (len(H) > 3) and (len(HmG) == 3)
    
            #print( '{}{}'.format(str(comb).ljust(40),comIdx) )
            #print('idx, T, Tcomp     = ', idx, T, Tc   )
            #print('idx, H, G         = ', idx, H, G   )
            #print('idx, Hmg   = ', idx, HmG )

            if hIsHidden:
                #pr.prettyPrint3DArray(Xcanidates)
                print(' {} {:2} has hidden triple {} at index {}'.format(house, idx, HmG, comIdx))
                myD = {'row': idx, 'tripVals': HmG, 'tripIdxs': comIdx }

                for tripIdx in myD['tripIdxs']:
                    temp  = [ x for x in Xcanidates[myD['row']][tripIdx] if x in myD['tripVals'] ]
                    inter = set.intersection( set(Xcanidates[myD['row']][tripIdx]), set(temp) )
                    diff  = set(Xcanidates[myD['row']][tripIdx]) - inter
                    if len(diff) != 0:
                        numPruned += len(diff)
                        print( '   Removed {} from {} {} index {}'.format(diff, house, myD['row'], myD['tripIdxs']) )
                    Xcanidates[myD['row']][tripIdx] = temp
                #pr.prettyPrint3DArray(Xcanidates)

                break

    if   house == 'row':  canidates = copy.deepcopy(Xcanidates)
    elif house == 'col':  canidates = mapRowsToCols(Xcanidates) 
    elif house == 'sqr':  canidates = mapRowsToSqrs(Xcanidates)
    #pr.prettyPrint3DArray(canidates)

    return(numPruned, canidates)

