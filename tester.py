import fillRoutines  as fr
from itertools import combinations
import pprint as pp
import printRoutines as pr

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

def pruneHiddenTriples(canidates, house, hiddenOrNaked):

    #pr.prettyPrint3DArray(canidates)
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
            #print('************', idx)
            if any(el == {0} for el in comb):    continue
            else:                                pass
            if any(len(el) == 1 for el in comb): continue
            else:                                pass

            T   = comIdx
            Tc  = [ x for x in range(0,len(rowOrColOrSqr)) if x not in T ]
            H  = set.union(*comb)
            G   = set(fr.flatten([ rowOrColOrSqr[ii] for ii in Tc if rowOrColOrSqr[ii] != [0]]))
            HmG = list(H - G)

            hIsNaked  = False
            hIsHidden = False

            if len(H) == 3:
                hIsNaked = True

            if (len(H) > 3) and (len(HmG) == 3):
                hIsHidden = True
                for c in comb:
                    inter = set.intersection(set(HmG), c)
                    if len(inter) == 0:
                        hIsHidden = False
                        break
    
            #print( '    {}{}'.format(str(comb).ljust(40),comIdx) )
            #print('    idx, T, Tcomp     = ', idx, T, Tc   )
            #print('    idx, H, G         = ', idx, H, G   )
            #print('    idx, Hmg   = ', idx, HmG )
            #print('    ',hIsNaked,hIsHidden)
                
            if hIsHidden and hiddenOrNaked == 'hidden':
                #pr.prettyPrint3DArray(Xcanidates)
                print(' {} {} has hidden triple {} at index {}'.format(house, idx, HmG, comIdx))
                myD = {'row': idx, 'tripVals': HmG, 'tripIdxs': comIdx }

                for tripIdx in myD['tripIdxs']:
                    temp  = [ x for x in rowOrColOrSqr[tripIdx] if x in myD['tripVals'] ]

                    inter = set.intersection( rowOrColOrSqr[tripIdx], set(temp) )
                    diff  = set(rowOrColOrSqr[tripIdx]) - inter
                    if len(diff) != 0:
                        numPruned += len(diff)
                        print( '   Removed {} from ({},{})'.format(diff, myD['row'], tripIdx) )

                    Xcanidates[myD['row']][tripIdx] = temp
                #pr.prettyPrint3DArray(Xcanidates)
                break

            if hIsNaked and hiddenOrNaked == 'naked':
                #pr.prettyPrint3DArray(Xcanidates)
                print(' {} {:2} has naked triple {} at index {}'.format(house, idx, H, comIdx))
                myD   = {'row': idx, 'tripVals': H, 'tripIdxs': comIdx }

                temp  = [ list(x) if kk in myD['tripIdxs'] else list(x-myD['tripVals']) for kk,x in enumerate(rowOrColOrSqr) ]
                temp2 = [ x if x != [0] else 0 for x in temp]

                for kk, el in enumerate(rowOrColOrSqr):
                    inter = set.intersection( el, set(temp[kk]) )
                    diff  = el - inter
                    if len(diff) != 0:
                        numPruned += len(diff)
                        #print( '   Removed {} from ({},{})'.format(       diff, myD['row'], tripIdx) )
                        print( '   Removed {} from ({},{})'.format(diff,  myD['row'], kk) )

                Xcanidates[myD['row']] = temp2
                #pr.prettyPrint3DArray(Xcanidates)
                break

    if   house == 'row':  canidates = copy.deepcopy(Xcanidates)
    elif house == 'col':  canidates = mapRowsToCols(Xcanidates) 
    elif house == 'sqr':  canidates = mapRowsToSqrs(Xcanidates)
    #pr.prettyPrint3DArray(canidates)

    return(numPruned, canidates)

if __name__ == '__main__':
    canidates = \
    [  #   x        ***    x   x      ***                *****
        [ [1,4,9], [1,8], [1,5,8,9], [3,8], [4,5], [7], [1,3,8], [6], [2] ], #  0. 3/3/3
        [ [1,2,3],          [1,2,3],       [1,2,3],   [7,3],       [8,1,2],   [9],     0,0,0 ], #  0. 3/3/3
        [ [1,2,3],          [1,2,3],       [1,2],     [7],       [8],   [9],     0,0,0 ], #  1. 3/3/2
        [ [1,2,3],          [1,2],         [1,3],     [7],       [8],   [9],     0,0,0 ], #  2. 3/2/2
        [ [1,2],            [1,3],         [2,3],     [7],       [8],   [9],     0,0,0 ], #  3. 2/2/2
        
        [ [1,2,3,4],        [1,2,3],       [1,2,3],   [7,4],     [8],   [9],     0,0,0 ], #  4. 3+/3/3
        [ [1,2,3,4],        [1,2,3,5],     [1,2,3],   [7,4,5],   [8],   [9],     0,0,0 ], #  5. 3+/3+/3
        [ [1,2,3,4],        [1,2,3,5],     [1,2,3,6], [7,4,5,6], [8],   [9],     0,0,0 ], #  6. 3+/3+/3+
        
        [ [1,2,3,4],        [1,2,3],       [1,2],     [7,4],     [8],   [9],     0,0,0 ], #  7. 3+/3/2
        #[ [1,2,3,4],        [1,2,3,5],     [1,2],     [7,4,5],   [8],   [9],     0,0,0 ], #  8. 3+/3+/2
        #[ [1,2,3,4],        [1,2,3,5],     [1,2],     [7,4,5,6], [8],   [9],     0,0,0 ], #  9. 3+/3+/2+
        #[ [1,2,3],          [1,2,3],       [1,2,4],   [7,4],     [8],   [9],     0,0,0 ], # 10. 3/3/2+
        #[ [1,2,3,4],        [1,2],         [1,3],     [7,4],     [8],   [9],     0,0,0 ], # 11. 3+/2/2
        #
        #[ [1,2,3,4],        [1,2,5],       [1,3],     [7,4,5],   [8],   [9],     0,0,0 ], # 12. 3+/2+/2
        #[ [1,2,3,4],        [1,2,5],       [1,3,6],   [7,4,5,6], [8],   [9],     0,0,0 ], # 13. 3+/2+/2+
        #[ [1,2,3],          [1,2,4],       [1,3,],    [7,4],     [8],   [9],     0,0,0 ], # 14. 3/2+/2
        #[ [1,2,3],          [1,2,4],       [1,3,5],   [7,4,5],   [8],   [9],     0,0,0 ], # 15. 3/2+/2+
        #
        #[ [1,2,4],          [1,3],         [2,3],     [7,4],     [8],   [9],     0,0,0 ], # 16. 2+/2/2
        #[ [1,2,4],          [1,3,5],       [2,3],     [7,4,5],   [8],   [9],     0,0,0 ], # 17. 2+/2+/2
        #[ [1,2,4],          [1,3,5],       [2,3,6],   [7,4,5,6], [8],   [9],     0,0,0 ], # 18. 2+/2+/2+
        #
        #[ [1,2,3,4],        [1,2,3,4],     [1,2,3,4], [7,4],     [8],   [9],     0,0,0 ], # 19. 3+a/3+a/3+a - Not found. Ok, its a naked quad.
        #[ [1,2,3,4],        [1,2,3,4],     [1,2,3,5], [7,4,5],   [8],   [9],     0,0,0 ], # 20. 3+a/3+a/3+b -
        #[ [1,2,3,4],        [1,2,3,5],     [1,2,3,4], [7,4,5],   [8],   [9],     0,0,0 ], # 21. 3+a/3+b/3+a -
        #[ [1,2,3,4],        [1,2,3,5],     [1,2,3,5], [7,4,5],   [6,8],   [9],     0,0,0 ], # 22. 3+a/3+b/3+b -
        #[ [1,2,3,5],        [1,2,3,4],     [1,2,3,4], [7,4,5],   [8],   [9],     0,0,0 ], # 23. 3+b/3+a/3+a -
        #[ [1,2,3,5],        [1,2,3,4],     [1,2,3,5], [7,4,5],   [8],   [9],     0,0,0 ], # 24. 3+b/3+a/3+b -
        #[ [1,2,3,5],        [1,2,3,5],     [1,2,3,4], [7,4,5],   [8],   [9],     0,0,0 ], # 25. 3+b/3+b/3+a -
        #[ [1,2,3,5],        [1,2,3,5],     [1,2,3,5], [7,5],     [8],   [9],     0,0,0 ], # 26. 3+b/3+b/3+b -
        #
        #[ [1,2,3,4],        [1,2,3,5,6],   [1,2,3,6],  [7,4,5,6],      [8],   [9],     0,0,0 ], # 27. 
        #[ [1,2,3,4],        [1,2,3,5],     [1,2,7],    [7],      [8],   [9],     0,0,0 ], # 28. 
        #[ [1,2,3,4],        [1,2,5],       [2,3,8],    [7],      [8],   [9],     0,0,0 ], # 29. 
        #[ [1,2,4],          [1,3,5],       [2,3,9],    [7],      [8],   [9],     0,0,0 ], # 30. 
        #[ [6,8,9],          [2,6,7,8,9],   [6,8,9],    [5,7],    [2,7], [2,5,7], 0,0,0 ], # 31. 
        #[ [1,2,3],          [1,4],         [2,5],      [7],      [8],   [9],     0,0,0 ], # 32. 
        
        #[ [2,4,5,6,7,8],    [2,4,5,6,7,8], [5,6,7],    [0],      [2],   [2,4,8], 0,0,0 ], # 33.
        #[ [1,3,7], [3,4,7], [3,4,7],       [1,8],      [1,5,8],  [5,6], [1,6],   0,0 ], # 34.
        #
    ]

    house = ['row']
    #house = ['row','col','sqr']
    for h in house:
        print('Pruning hidden triples in {} ************************************************ Start.'.format(h))
        totNumPruned  = 0
        loopNumPruned = 1
        while loopNumPruned:
            #loopNumPruned, canidates = pruneHiddenTriples(canidates, h, 'hidden')
            loopNumPruned, canidates = pruneHiddenTriples(canidates, h, 'naked')
            totNumPruned  += loopNumPruned
        print('Pruning hidden triples in {} ** ( total pruned =  {:2} ) ************************ End.'.format(h, totNumPruned))

