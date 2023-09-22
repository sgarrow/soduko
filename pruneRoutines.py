import fillRoutines  as fr
from itertools import combinations
import pprint as pp
import printRoutines as pr
import mapping as mp

def pruneNakedAndHiddenTuples(canidates, house, hiddenOrNaked, N):

    #pr.printCanidates(canidates)
    import copy
    if   house == 'row':  Xcanidates = copy.deepcopy(canidates)
    elif house == 'col':  Xcanidates = mp.mapColsToRows(canidates) 
    elif house == 'sqr':  Xcanidates = mp.mapSrqsToRows(canidates)

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
                #print(' {} {} has hidden {}-tuple {} at index {}'.format(house, idx, N, HmG, comIdx))
                myD = {'row': idx, 'tripVals': HmG, 'tripIdxs': comIdx }

                for tripIdx in myD['tripIdxs']:
                    temp  = [ x for x in rowOrColOrSqr[tripIdx] if x in myD['tripVals'] ]

                    inter = set.intersection( rowOrColOrSqr[tripIdx], set(temp) )
                    diff  = set(rowOrColOrSqr[tripIdx]) - inter
                    if len(diff) != 0:
                        numPruned += len(diff)
                        #print( '   Removed {} from ({},{})'.format(diff, myD['row'], tripIdx) )

                    Xcanidates[myD['row']][tripIdx] = temp
                #pr.printCanidates(Xcanidates)
                break

            if hIsNaked and hiddenOrNaked == 'naked':
                #pr.printCanidates(Xcanidates)
                #print(' {} {} has naked {}-tuple {} at index {}'.format(house, idx, N, H, comIdx))
                myD   = {'row': idx, 'tripVals': H, 'tripIdxs': comIdx }

                temp  = [ list(x) if kk in myD['tripIdxs'] else list(x-myD['tripVals']) for kk,x in enumerate(rowOrColOrSqr) ]
                temp2 = [ x if x != [0] else 0 for x in temp]

                for kk, el in enumerate(rowOrColOrSqr):
                    inter = set.intersection( el, set(temp[kk]) )
                    diff  = el - inter
                    if len(diff) != 0:
                        numPruned += len(diff)
                        #print( '   Removed {} from ({},{})'.format(diff,  myD['row'], kk) )

                Xcanidates[myD['row']] = temp2
                #pr.printCanidates(Xcanidates)
                break

    if   house == 'row':  canidates = copy.deepcopy(Xcanidates)
    elif house == 'col':  canidates = mp.mapRowsToCols(Xcanidates) 
    elif house == 'sqr':  canidates = mp.mapRowsToSqrs(Xcanidates)
    #pr.printCanidates(canidates)

    return(numPruned, canidates)
############################################################################

def pruneXwings(canidates, house):
    #pr.printCanidates(canidates)
    import copy
    if   house == 'row':  Xcanidates = copy.deepcopy(canidates)
    elif house == 'col':  Xcanidates = mp.mapColsToRows(canidates) 

    numPruned = 0

    allBinsHeightTwo = []
    for row in Xcanidates:
        flatRow = fr.flatten(row)
        histRow = fr.genHistogram(flatRow)
        allBinsHeightTwo.append([ x[0] for x in histRow if x[1] == 2 and x[0] != 0])
    #pp.pprint(allBinsHeightTwo)

    k = 0
    myD = {}
    for idx,lstOfVals in enumerate(allBinsHeightTwo):
        for val in lstOfVals:
            cols = [ c for c,lst in enumerate(Xcanidates[idx]) if lst != 0 and val in lst ]
            #print(' in row {}, {} appears exactly twice - cols {}'.format(idx, val, cols))
            myD[k] = { 'A_row':idx, 'B_cols':cols, 'C_val':val,  }
            k += 1
    #pp.pprint(myD)

    k = 0
    xWingD = {}
    combSet = combinations(myD.values(), 2)
    for c in combSet:
        #print(c)
        if c[0]['C_val'] == c[1]['C_val'] and c[0]['B_cols'] == c[1]['B_cols']:

            xWingD[k] = { 'A_rows': [ c[0]['A_row'], c[1]['A_row'] ],
                          'B_cols':   c[0]['B_cols'],
                          'C_val' :   c[0]['C_val']  }
            k += 1
    #pp.pprint(xWingD)

    for xw in xWingD.values():
        for rIdx,row in enumerate(Xcanidates):
            for cIdx in xw['B_cols']:
                if rIdx not in xw['A_rows'] and Xcanidates[rIdx][cIdx] != 0 and xw['C_val'] in Xcanidates[rIdx][cIdx]:
                    #pr.printCanidates(Xcanidates)
                    Xcanidates[rIdx][cIdx].remove(xw['C_val'])
                    #print('remove {} from ({},{})'.format(xw['C_val'], rIdx, cIdx))
                    #pr.printCanidates(Xcanidates)
                    numPruned += 1

    if   house == 'row':  canidates = copy.deepcopy(Xcanidates)
    elif house == 'col':  canidates = mp.mapRowsToCols(Xcanidates) 
    #print(house)

    return(numPruned, canidates)
############################################################################

# map sqrs to rows -> Xcanidates
# 
# find all numbers in rows of Xcanidates that appear exactly twice 
# 
# if the nums that appear exactly twice are in cols 
# 0,1,2 or 3,4,5 of 6,7,8 then they are in the same row of canidates
# and hence are a 'row' pointing pair.
# 
# if the nums that appear exactly twice are in cols 
# 0,3,6 or 1,4,7 of 2,5,8 then they are in the same col of canidates
# and hence are a 'col' pointing pair.
#
# process the pointing pairs in canidates.

def prunePointingPairs(canidates):
    Xcanidates = mp.mapSrqsToRows(canidates)

    #printCanidates(canidates)
    #printCanidates(Xcanidates)

    numPruned = 0

    allBinsHeightTwo = []
    for row in Xcanidates:
        flatRow = fr.flatten(row)
        histRow = fr.genHistogram(flatRow)
        allBinsHeightTwo.append([ x[0] for x in histRow if x[1] == 2 and x[0] != 0])
    pp.pprint(allBinsHeightTwo)
    print()

    k = 0
    myD = {}
    for idx,lstOfVals in enumerate(allBinsHeightTwo):
        for val in lstOfVals:
            cols = [ c for c,lst in enumerate(Xcanidates[idx]) if lst != 0 and val in lst ]
            #print(' in row {}, {} appears exactly twice - cols {}'.format(idx, val, cols))
            myD[k] = { 'A_sqr':idx, 'B_idxs':cols, 'C_val':val,  }
            k += 1
    #pp.pprint(myD)

    k = 0
    ppD = {}
    for v in myD.values():
        #print(v)
        diff = v['B_idxs'][1] - v['B_idxs'][0]
        sameRem = v['B_idxs'][1]//3 == v['B_idxs'][0]//3
        if diff < 3 and sameRem:
            ppD[k] = v
        k += 1
    #pp.pprint(ppD)


    k = 0
    ppD2 = {}
    for v in ppD.values():
        r0,c0 = mp.getRowColFromSqrOffset(v['A_sqr'],v['B_idxs'][0])
        r1,c1 = mp.getRowColFromSqrOffset(v['A_sqr'],v['B_idxs'][1])
        if r0 != r1:
            print('SANITY CHECK')
            exit()
        print('    square {} has row pointing pair on row {} cols {},{} (val={})'.\
            format(v['A_sqr'],r0,c0,c1,v['C_val']))
        ppD2[k] = { 'aRow':r0, 'bCols':[c0,c1], 'cVal':v['C_val'] }
        k += 1
    pp.pprint(ppD2)

    rowsProcessed = []
    for v in ppD2.values():
        if v['aRow'] not in rowsProcessed:
            cols = [ x for x in range(9) if x not in v['bCols'] ]
            for c in cols:
                if canidates[v['aRow']][c] != 0 and v['cVal'] in canidates[v['aRow']][c]:
                    canidates[ v['aRow']][c].remove(v['cVal'])
                    print('    removed {} from {},{}'.\
                        format(v['cVal'], v['aRow'], c))
                    numPruned += 1


    #pr.printCanidates(canidates)
    return numPruned,canidates
############################################################################

