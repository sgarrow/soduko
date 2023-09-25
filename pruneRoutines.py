'''docstr'''
import sys
import copy
from itertools import combinations
import pprint as pp
import fillRoutines  as fr
import mapping as mp
def pruneNakedAndHiddenTuples(canidates, house, hiddenOrNaked, tupSiz):
    '''docstr'''
    #pr.printCanidates(canidates)

    cpyDic = {'row':copy.deepcopy, 'col':mp.mapColsToRows, 'sqr':mp.mapSrqsToRows}
    xCanidates = cpyDic[house](canidates)

    numPruned = 0
    for idx, rowOrColOrSqrWithZeros in enumerate(xCanidates):
        rOrCOrS = [set(x) if x != 0 else set([0]) for x in rowOrColOrSqrWithZeros]
        combSet = combinations(rOrCOrS, tupSiz)  # C(n,r) = n! / ( r! * (n-r)! ). C(9,3)=84.
        if tupSiz == 2:
            combIdxs = \
            list((i,j) for ((i,_),(j,_)) in combinations(enumerate(rOrCOrS), tupSiz))
        elif tupSiz == 3:
            combIdxs = \
            list((i,j,k) for ((i,_),(j,_),(k,_)) in combinations(enumerate(rOrCOrS), tupSiz))
        elif tupSiz == 4:
            combIdxs = \
            list((i,j,k,l) for ((i,_),(j,_),(k,_),(l,_)) in \
                combinations(enumerate(rOrCOrS), tupSiz))
        elif tupSiz == 5:
            combIdxs = \
            list((i,j,k,l,m) for ((i,_),(j,_),(k,_),(l,_),(m,_)) in \
                combinations(enumerate(rOrCOrS), tupSiz))

        for comb,comIdx in zip(combSet,combIdxs):
            if any(el == {0} for el in comb) or any(len(el) == 1 for el in comb):
                continue

            comIdxC  = [ x for x in range(0,len(rOrCOrS)) if x not in comIdx ]
            setH  = set.union(*comb)
            setG   = set(fr.flatten([ rOrCOrS[ii] for ii in comIdxC if rOrCOrS[ii] != [0]]))
            lstHmG = list(setH - setG)

            hIsNaked = len(setH) == tupSiz

            hIsHidden = False
            if (len(setH) > tupSiz) and (len(lstHmG) == tupSiz):
                hIsHidden = True
                for aComb in comb:
                    inter = set.intersection(set(lstHmG), aComb)
                    if len(inter) == 0:
                        hIsHidden = False
                        break

            #print( '    {}{}'.format(str(comb).ljust(40),comIdx) )
            #print('    idx, comIdx, Tcomp     = ', idx, comIdx, comIdxC   )
            #print('    idx, H, G         = ', idx, H, G   )
            #print('    idx, Hmg   = ', idx, HmG )
            #print('    ',hIsNaked,hIsHidden)

            if hIsHidden and hiddenOrNaked == 'hidden':
                #pr.printCanidates(xCanidates)
                #print(' {} {} has hidden {}-tuple {} at index {}'.\
                # format(house,idx,tupSiz,HmG,comIdx))
                myD = {'row': idx, 'tripVals': lstHmG, 'tripIdxs': comIdx }

                for tripIdx in myD['tripIdxs']:
                    temp  = [ x for x in rOrCOrS[tripIdx] if x in myD['tripVals'] ]

                    inter = set.intersection( rOrCOrS[tripIdx], set(temp) )
                    diff  = set(rOrCOrS[tripIdx]) - inter
                    if len(diff) != 0:
                        numPruned += len(diff)
                        #print( '   Removed {} from ({},{})'.format(diff, myD['row'], tripIdx) )

                    xCanidates[myD['row']][tripIdx] = temp
                #pr.printCanidates(xCanidates)
                break

            if hIsNaked and hiddenOrNaked == 'naked':
                #pr.printCanidates(xCanidates)
                #print(' {} {} has naked {}-tuple {} at index {}'.\
                # format(house, idx, tupSiz, H, comIdx))
                myD   = {'row': idx, 'tripVals': setH, 'tripIdxs': comIdx }

                temp  = [ list(x) if kk in myD['tripIdxs'] else \
                          list(x-myD['tripVals']) for kk,x in enumerate(rOrCOrS) ]
                temp2 = [ x if x != [0] else 0 for x in temp]

                for idx, elem in enumerate(rOrCOrS):
                    inter = set.intersection( elem, set(temp[idx]) )
                    diff  = elem - inter
                    if len(diff) != 0:
                        numPruned += len(diff)
                        #print( '   Removed {} from ({},{})'.format(diff,  myD['row'], idx) )

                xCanidates[myD['row']] = temp2
                #pr.printCanidates(xCanidates)
                break

    cpyDic = {'row':copy.deepcopy, 'col':mp.mapRowsToCols, 'sqr':mp.mapRowsToSqrs}
    canidates = cpyDic[house](xCanidates)

    #pr.printCanidates(canidates)

    return(numPruned, canidates)
############################################################################

def pruneXwings(canidates, house):
    '''docstr'''
    #pr.printCanidates(canidates)

    cpyDic = {'row':copy.deepcopy, 'col':mp.mapColsToRows, 'sqr':mp.mapSrqsToRows}
    xCanidates = cpyDic[house](canidates)

    numPruned = 0

    allBinsHeightTwo = []
    for row in xCanidates:
        flatRow = fr.flatten(row)
        histRow = fr.genHistogram(flatRow)
        allBinsHeightTwo.append([ x[0] for x in histRow if x[1] == 2 and x[0] != 0])
    #pp.pprint(allBinsHeightTwo)

    k = 0
    myD = {}
    for idx,lstOfVals in enumerate(allBinsHeightTwo):
        for val in lstOfVals:
            cols = [ c for c,lst in enumerate(xCanidates[idx]) if lst != 0 and val in lst ]
            #print(' in row {}, {} appears exactly twice - cols {}'.format(idx, val, cols))
            myD[k] = { 'A_row':idx, 'B_cols':cols, 'C_val':val,  }
            k += 1
    #pp.pprint(myD)

    k = 0
    xWingD = {}
    combSet = combinations(myD.values(), 2)
    for comb in combSet:
        #print(comb)
        if comb[0]['C_val'] == comb[1]['C_val'] and comb[0]['B_cols'] == comb[1]['B_cols']:

            xWingD[k] = { 'A_rows': [ comb[0]['A_row'], comb[1]['A_row'] ],
                          'B_cols':   comb[0]['B_cols'],
                          'C_val' :   comb[0]['C_val']  }
            k += 1
    #pp.pprint(xWingD)

    for xWing in xWingD.values():
        for rIdx,row in enumerate(xCanidates):
            for cIdx in xWing['B_cols']:
                if (rIdx not in xWing['A_rows'])  and \
                    (row[cIdx] != 0) and \
                    (xWing['C_val'] in row[cIdx]):
                    #pr.printCanidates(xCanidates)
                    xCanidates[rIdx][cIdx].remove(xWing['C_val'])
                    #print('remove {} from ({},{})'.format(xw['C_val'], rIdx, cIdx))
                    #pr.printCanidates(xCanidates)
                    numPruned += 1

    cpyDic = {'row':copy.deepcopy, 'col':mp.mapRowsToCols, 'sqr':mp.mapRowsToSqrs}
    canidates = cpyDic[house](xCanidates)

    return(numPruned, canidates)
############################################################################

# map sqrs to rows -> xCanidates
#
# find all numbers in rows of xCanidates that appear exactly twice
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
    '''docstr'''
    xCanidates = mp.mapSrqsToRows(canidates)

    #printCanidates(canidates)
    #printCanidates(xCanidates)

    numPruned = 0

    allBinsHeightTwo = []
    for row in xCanidates:
        flatRow = fr.flatten(row)
        histRow = fr.genHistogram(flatRow)
        allBinsHeightTwo.append([ x[0] for x in histRow if x[1] == 2 and x[0] != 0])
    pp.pprint(allBinsHeightTwo)
    print()

    k = 0
    myD = {}
    for idx,lstOfVals in enumerate(allBinsHeightTwo):
        for val in lstOfVals:
            cols = [ c for c,lst in enumerate(xCanidates[idx]) if lst != 0 and val in lst ]
            #print(' in row {}, {} appears exactly twice - cols {}'.format(idx, val, cols))
            myD[k] = { 'A_sqr':idx, 'B_idxs':cols, 'C_val':val,  }
            k += 1
    #pp.pprint(myD)

    k = 0
    ppD = {}
    for val in myD.values():
        #print(val)
        diff = val['B_idxs'][1] - val['B_idxs'][0]
        sameRem = val['B_idxs'][1]//3 == val['B_idxs'][0]//3
        if diff < 3 and sameRem:
            ppD[k] = val
        k += 1
    #pp.pprint(ppD)

    k = 0
    ppD2 = {}
    for val in ppD.values():
        row0,col0 = mp.getRowColFromSqrOffset(val['A_sqr'],val['B_idxs'][0])
        row1,col1 = mp.getRowColFromSqrOffset(val['A_sqr'],val['B_idxs'][1])
        if row0 != row1:
            print('SANITY CHECK')
            sys.exit()
        print('    square {} has row pointing pair on row {} cols {},{} (val={})'.\
            format(val['A_sqr'],row0,col0,col1,val['C_val']))
        ppD2[k] = { 'aRow':row0, 'bCols':[col0,col1], 'cVal':val['C_val'] }
        k += 1
    pp.pprint(ppD2)

    rowsProcessed = []
    for val in ppD2.values():
        if val['aRow'] not in rowsProcessed:
            cols = [ x for x in range(9) if x not in val['bCols'] ]
            for cIdx in cols:
                if canidates[val['aRow']][cIdx]!=0 and val['cVal'] in canidates[val['aRow']][cIdx]:
                    canidates[ val['aRow']][cIdx].remove(val['cVal'])
                    print('    removed {} from {},{}'.format(val['cVal'], val['aRow'], cIdx))
                    numPruned += 1

    #pr.printCanidates(canidates)
    return numPruned,canidates
############################################################################
