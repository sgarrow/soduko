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

    #pr.prettyPrint3DArray(canidates)
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
        elif N == 4:
            combIdxs = list((i,j,k,l) for ((i,_),(j,_),(k,_),(l,_)) in combinations(enumerate(rowOrColOrSqr), N))
        elif N == 5:
            combIdxs = list((i,j,k,l,m) for ((i,_),(j,_),(k,_),(l,_),(m,_)) in combinations(enumerate(rowOrColOrSqr), N))

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
                #pr.prettyPrint3DArray(Xcanidates)
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
                #pr.prettyPrint3DArray(Xcanidates)
                break

            if hIsNaked and hiddenOrNaked == 'naked':
                #pr.prettyPrint3DArray(Xcanidates)
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
                #pr.prettyPrint3DArray(Xcanidates)
                break

    if   house == 'row':  canidates = copy.deepcopy(Xcanidates)
    elif house == 'col':  canidates = mapRowsToCols(Xcanidates) 
    elif house == 'sqr':  canidates = mapRowsToSqrs(Xcanidates)
    #pr.prettyPrint3DArray(canidates)

    return(numPruned, canidates)
