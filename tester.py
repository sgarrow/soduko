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

def pruneHiddenTriples(canidates, house, hiddenOrNaked, N):

    #pr.printCanidates(canidates)
    import copy
    if   house == 'row':  Xcanidates = copy.deepcopy(canidates)
    elif house == 'col':  Xcanidates = mapColsToRows(canidates) 
    elif house == 'sqr':  Xcanidates = mapSrqsToRows(canidates)

    numPruned = 0
    for idx, rowOrColOrSqrWithZeros in enumerate(Xcanidates):
        rowOrColOrSqr = [set(x) if x != 0 else set([0]) for x in rowOrColOrSqrWithZeros]
        combSet       = combinations(rowOrColOrSqr, N)  # C(n,r) = n! / ( r! * (n-r)! ). C(9,3) = 84.
        if N == 2:
            combIdxs = list((i,j) for ((i,_),(j,_)) in combinations(enumerate(rowOrColOrSqr), N))
        elif N == 3:
            combIdxs = list((i,j,k) for ((i,_),(j,_),(k,_)) in combinations(enumerate(rowOrColOrSqr), N))

        for comb,comIdx in zip(combSet,combIdxs):
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

            if len(H) == N:
                hIsNaked = True

            if (len(H) > N) and (len(HmG) == N):
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
                #pr.printCanidates(Xcanidates)
                print(' {} {} has hidden {}-tuple {} at index {}'.format(house, idx, N, HmG, comIdx))
                myD = {'row': idx, 'tripVals': HmG, 'tripIdxs': comIdx }

                for tripIdx in myD['tripIdxs']:
                    temp  = [ x for x in rowOrColOrSqr[tripIdx] if x in myD['tripVals'] ]

                    inter = set.intersection( rowOrColOrSqr[tripIdx], set(temp) )
                    diff  = set(rowOrColOrSqr[tripIdx]) - inter
                    if len(diff) != 0:
                        numPruned += len(diff)
                        print( '   Removed {} from ({},{})'.format(diff, myD['row'], tripIdx) )

                    Xcanidates[myD['row']][tripIdx] = temp
                #pr.printCanidates(Xcanidates)
                break

            if hIsNaked and hiddenOrNaked == 'naked':
                #pr.printCanidates(Xcanidates)
                print(' {} {} has naked {}-tuple {} at index {}'.format(house, idx, N, H, comIdx))
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
                #pr.printCanidates(Xcanidates)
                break

    if   house == 'row':  canidates = copy.deepcopy(Xcanidates)
    elif house == 'col':  canidates = mapRowsToCols(Xcanidates) 
    elif house == 'sqr':  canidates = mapRowsToSqrs(Xcanidates)
    #pr.printCanidates(canidates)

    return(numPruned, canidates)
############################################################################

def printCanidates(canidates):
    for rIdx,row in enumerate(canidates):     # for each row
        print('++------+------+------++------+------+------++------+------+------++')
        for ii in range(3):   # print 3 lines.
            thingsToPrint = list(range( ii*3+1, ii*3+4 )) # 1,2,3; 4,5,6; 7,8,9
            #print(thingsToPrint)
            print('|',end = '')
            for cIdx,cell in enumerate(row):
                for num in thingsToPrint:
                    if (num-1)%3 == 0: print('|',end = '')
                    if cell != 0 and num in cell:
                        print('{:2}'.format(num), end = '')
                    else:
                        print('  ',end = '')
                #if cIdx in [2,5]:  print('|',end = '') 
                if (cIdx+1)%3 == 0:  print('|',end = '') 
            print('|') # output 1st, 2nd or 3rd line of the row
        if (rIdx+1)%3 ==0:
            print('++------+------+------++------+------+------++------+------+------++')
    return 0
############################################################################

if __name__ == '__main__':
    canidates = \
    [
        #[ [1,2,3,4,5,6,7,8,9], [1],[2],[3],[4],[5],[6],[7],[8] ],
        [ [1,2,3,4,5,6,7,8,9], [1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        [ [1,2,3,4,5,6,7,8,9], [1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        [ [1,2,3,4,5,6,7,8,9], [1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        [ [1,2,3,4,5,6,7,8,9], [1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        [ [1,2,3,4,5,6,7,8,9], [1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        [ [1,2,3,4,5,6,7,8,9], [1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        [ [1,2,3,4,5,6,7,8,9], [1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        [ [1,2,3,4,5,6,7,8,9], [1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        [ 0, [        5,6,7,8  ],[                9],[      4,5,6,     ],[  2,  4,  6,  8, ],[    3,4,5,       ],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
        #[ [1,2,3,4,5,6,7,8,9], [8],[7],[6],[5],[4],[3],[2],[1] ],
        #[ [1,2,3,4,5,6,7,8,9], [8],[7],[6],[5],[4],[3],[2],[1] ],
        #[ [1,2,3,4,5,6,7,8,9], [8],[7],[6],[5],[4],[3],[2],[1] ],
        #[ [1,2,3,4,5,6,7,8,9], [8],[7],[6],[5],[4],[3],[2],[1] ],
        #[ [1,2,3,4,5,6,7,8,9], [8],[7],[6],[5],[4],[3],[2],[1] ],
        #[ [1,2,3,4,5,6,7,8,9], [8],[7],[6],[5],[4],[3],[2],[1] ],
        #[ [1,2,3,4,5,6,7,8,9], [8],[7],[6],[5],[4],[3],[2],[1] ],
        #[ [1,2,3,4,5,6,7,8,9], [8],[7],[6],[5],[4],[3],[2],[1] ],
        #[ [1,2,3],[1,2], [3],[4],[5],[6],[7],[8],[9] ],
        #[ [1,2],[1,2], [3],[4],[5],[6],[7],[8],[9] ],
        #[ [1,2],[1,2], [3],[4],[5],[6],[7],[8],[9] ],
        #[ [1,2],[1,2], [3],[4],[5],[6],[7],[8],[9] ],
        #[ [1,2],[1,2], [3],[4],[5],[6],[7],[8],[9] ],
        #[ [1,2],[1,2], [3],[4],[5],[6],[7],[8],[9] ],
        #[ [1,2],[1,2], [3],[4],[5],[6],[7],[8],[9] ],
        #[ [1,2],[1,2], [3],[4],[5],[6],[7],[8],[9] ],
        #[ [1,2],[1,2], [3],[4],[5],[6],[7],[8],[9] ],


        #   x        ___    x   x      ___                _____
        #[ [1,4,9], [1,8], [1,5,8,9], [3,8], [4,5], [7], [1,3,8], [6], [2] ], #  0. 3/3/3
        #[ [1,2,3],          [1,2,3],       [1,2,3],   [7,3],       [8,1,2],   [9],     0,0,0 ], #  0. 3/3/3
        #[ [1,2,3],          [1,2,3],       [1,2],     [7],       [8],   [9],     0,0,0 ], #  1. 3/3/2
        #[ [1,2,3],          [1,2],         [1,3],     [7],       [8],   [9],     0,0,0 ], #  2. 3/2/2
        #[ [1,2],            [1,3],         [2,3],     [7],       [8],   [9],     0,0,0 ], #  3. 2/2/2
        #
        #[ [1,2,3,4],        [1,2,3],       [1,2,3],   [7,4],     [8],   [9],     0,0,0 ], #  4. 3+/3/3
        #[ [1,2,3,4],        [1,2,3,5],     [1,2,3],   [7,4,5],   [8],   [9],     0,0,0 ], #  5. 3+/3+/3
        #[ [1,2,3,4],        [1,2,3,5],     [1,2,3,6], [7,4,5,6], [8],   [9],     0,0,0 ], #  6. 3+/3+/3+
        #
        #[ [1,2,3,4],        [1,2,3],       [1,2],     [7,4],     [8],   [9],     0,0,0 ], #  7. 3+/3/2
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

    printCanidates(canidates)
    #house = ['row']
    ##house = ['row','col','sqr']
    #for h in house:
    #    print('Pruning hidden triples in {} Start.'.format(h))
    #    totNumPruned  = 0
    #    loopNumPruned = 1
    #    while loopNumPruned:
    #        loopNumPruned, canidates = pruneHiddenTriples(canidates, h, 'hidden', 2)
    #        #loopNumPruned, canidates = pruneHiddenTriples(canidates, h, 'naked', 2)
    #        totNumPruned  += loopNumPruned
    #    print('Pruning hidden triples in {} * ( total pruned =  {:2} ) * End.'.format(h, totNumPruned))

