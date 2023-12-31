import sys
import copy
from itertools import combinations
import pprint  as pp
import mapping as mp
import fillRoutines  as fr
import printRoutines as pr

def getComIdxs(rOrCOrS, tupSiz):
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
    return combIdxs
############################################################################
def pruneNakedAndHiddenTuples(canidates, house, hiddenOrNaked, tupSiz, clArgs):
    #pr.printCanidates(canidates)

    cpyDic = {'row':copy.deepcopy, 'col':mp.mapColsToRows, 'sqr':mp.mapSrqsToRows}
    xCanidates = cpyDic[house](canidates)

    numPruned = 0
    for idx, rowOrColOrSqrWithZeros in enumerate(xCanidates):
        rOrCOrS = [set(x) if x != 0 else set([0]) for x in rowOrColOrSqrWithZeros]
        combSet = combinations(rOrCOrS, tupSiz)  # C(n,r) = n! / ( r! * (n-r)! ). C(9,3)=84.
        combIdxs = getComIdxs(rOrCOrS, tupSiz)

        for comb,comIdx in zip(combSet,combIdxs):
            if any(el == {0} for el in comb) or any(len(el) == 1 for el in comb):
                continue

            comIdxC = [ x for x in range(0,len(rOrCOrS)) if x not in comIdx ]
            setH    = set.union(*comb)
            setG    = set(fr.flatten([ rOrCOrS[ii] for ii in comIdxC if rOrCOrS[ii] != [0]]))
            lstHmG  = list(setH - setG)

            hIsNaked = len(setH) == tupSiz

            hIsHidden = False
            if (len(setH) > tupSiz) and (len(lstHmG) == tupSiz):
                hIsHidden = True
                for aComb in comb:
                    if len(set.intersection(set(lstHmG), aComb) ) == 0:
                        hIsHidden = False
                        break

            if hIsHidden and hiddenOrNaked == 'hidden':
                myD = {'row': idx, 'tripVals': lstHmG, 'tripIdxs': comIdx }
                if 'nhtPrn' in clArgs: pr.printCanidates(xCanidates)
                if 'nhtPrn' in clArgs: print('Hidden')
                if 'nhtPrn' in clArgs: pp.pprint(myD)
            
                for tripIdx in myD['tripIdxs']:
                    temp  = [ x for x in rOrCOrS[tripIdx] if x in myD['tripVals'] ]
                    diff  = set(rOrCOrS[tripIdx]) - set.intersection( rOrCOrS[tripIdx], set(temp) )
                    if len(diff) != 0:
                        numPruned += len(diff)
                        if 'nhtPrn' in clArgs: print( '      remove {} from ({},{})'.format(diff, myD['row'], tripIdx) )
            
                    xCanidates[myD['row']][tripIdx] = temp
                if 'nhtPrn' in clArgs: pr.printCanidates(xCanidates)
                break

            if hIsNaked and hiddenOrNaked == 'naked':
                myD   = {'row': idx, 'tripVals': setH, 'tripIdxs': comIdx }
                if 'nhtPrn' in clArgs: pr.printCanidates(xCanidates)
                if 'nhtPrn' in clArgs: print('Naked')
                if 'nhtPrn' in clArgs: pp.pprint(myD)

                temp  = [ list(x) if kk in myD['tripIdxs'] else \
                          list(x-myD['tripVals']) for kk,x in enumerate(rOrCOrS) ]
                temp2 = [ x if x != [0] else 0 for x in temp]

                for idx, elem in enumerate(rOrCOrS):
                    diff  = elem - set.intersection( elem, set(temp[idx]) )
                    if len(diff) != 0:
                        numPruned += len(diff)
                        if 'nhtPrn' in clArgs: print( '      remove {} from ({},{})'.format(diff,  myD['row'], idx) )

                xCanidates[myD['row']] = temp2
                if 'nhtPrn' in clArgs: pr.printCanidates(xCanidates)
                break

    cpyDic = {'row':copy.deepcopy, 'col':mp.mapRowsToCols, 'sqr':mp.mapRowsToSqrs}
    canidates = cpyDic[house](xCanidates)

    #pr.printCanidates(canidates)

    return(numPruned, canidates)
############################################################################

def pruneXwings(canidates, house, clArgs):
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

    didRemove = False
    for xWing in xWingD.values():
        for rIdx,row in enumerate(xCanidates):
            for cIdx in xWing['B_cols']:
                if (rIdx not in xWing['A_rows'])  and \
                    (row[cIdx] != 0) and \
                    (xWing['C_val'] in row[cIdx]):
                    xCanidates[rIdx][cIdx].remove(xWing['C_val'])

                    if not didRemove and 'xwPrn' in clArgs:
                        pr.printCanidates(xCanidates)
                        pp.pprint(xWingD)
                        didRemove = True
                    if 'xwPrn' in clArgs: print('   remove {} from ({},{})'.format(xWing['C_val'], rIdx, cIdx))
                    numPruned += 1

    if didRemove: pr.printCanidates(xCanidates)
    cpyDic = {'row':copy.deepcopy, 'col':mp.mapRowsToCols, 'sqr':mp.mapRowsToSqrs}
    canidates = cpyDic[house](xCanidates)

    return(numPruned, canidates)
############################################################################

# map sqrs to rows -> xCanidates
#
# find all nums in rows of xCanidates (sqrs of canidates) that appear exactly twice
#
# if the nums that appear exactly twice are in cols of xCanidates (sqrs of canidates)
# 0,1,2 or 3,4,5 of 6,7,8 then they are in the same row of canidates
# and hence are a 'row' pointing pair.
#
# if the nums that appear exactly twice are in cols of xCanidates (sqrs of canidates) 
# 0,3,6 or 1,4,7 of 2,5,8 then they are in the same col of canidates
# and hence are a 'col' pointing pair.
#
# process the pointing pairs in canidates.

def prunePointingPairs(canidates, house, clArgs):

    xCanidates = mp.mapSrqsToRows(canidates)
    numPruned  = 0

    # find all nums in rows of xCanidates (sqrs of canidates) that appear exactly twice
    allBinsHeightTwo = []
    for row in xCanidates:
        flatRow = fr.flatten(row)
        histRow = fr.genHistogram(flatRow)
        allBinsHeightTwo.append([ x[0] for x in histRow if x[1] == 2 and x[0] != 0])
    ####################################################################################

    # Place above data in a dict and add to data the two offset within the square 
    # where the two nums appear. Note that pair may not be on the same row/col ...
    k = 0
    allBinsHeightTwoD = {}
    for idx,lstOfVals in enumerate(allBinsHeightTwo):
        for val in lstOfVals:
            cols = [ c for c,lst in enumerate(xCanidates[idx]) if lst != 0 and val in lst ]
            allBinsHeightTwoD[k] = { 'A_sqr':idx, 'B_idxs':cols, 'C_val':val,  }
            k += 1
    ####################################################################################

    # Create a new dict (either row or col, but not both) that are a subset of above dict.
    # New dict only contains the elements of the old dict that have the pair (in the square)
    # on the same row/col.  One of the two dicts will be empty.
    k = 0
    ppRowRqmt = [[0,1,2],[3,4,5],[6,7,8]]
    ppColRqmt = [[0,3,6],[1,4,7],[2,5,8]]
    ppRowD = {}
    ppColD = {}
    if house == 'row': rqmt = ppRowRqmt
    if house == 'col': rqmt = ppColRqmt
    for val in allBinsHeightTwoD.values():
        for el in rqmt:
            if all(x in el for x in val['B_idxs']):
                if house == 'row': ppRowD[k] = val
                if house == 'col': ppColD[k] = val
                k += 1
    ####################################################################################

    # create a 3rd dict (either row or col, but not both) that is the same as the above 
    # dict except sqr,offset mapped to abs r,c.
    k = 0
    ppRowAbsCoordD = {}
    ppColAbsCoordD = {}
    if house == 'row': ppD = ppRowD
    if house == 'col': ppD = ppColD
    for val in ppD.values():
        row0,col0 = mp.getRowColFromSqrOffset(val['A_sqr'],val['B_idxs'][0])
        row1,col1 = mp.getRowColFromSqrOffset(val['A_sqr'],val['B_idxs'][1])
        if house == 'row': ppRowAbsCoordD[k] = { 'aRow':row0, 'bCols':[col0,col1], 'cVal':val['C_val'] }
        if house == 'col': ppColAbsCoordD[k] = { 'aCol':col0, 'bRows':[row0,row1], 'cVal':val['C_val'] }
        k += 1
    ####################################################################################

    # debug prints
    if 'ppPrn' in clArgs:
        thingsPprint = { 'allBinsHeightTwo':allBinsHeightTwo,
                         'allBinsHeightTwoD':allBinsHeightTwoD,
                         'ppRowD':ppRowD,
                         'ppColD':ppColD,
                         'ppRowAbsCoordD':ppRowAbsCoordD,
                         'ppColAbsCoordD':ppColAbsCoordD }

        print('canidates')
        pr.printCanidates(canidates)
        print()
        for k,v in thingsPprint.items():
            print(k)
            pp.pprint(v)
            print()
    ####################################################################################

    # perform associated removals Note only one of the 2 dicts looped through below will 
    # have anything in it.
    rowsProcessed = []
    for val in ppRowAbsCoordD.values():
        if val['aRow'] not in rowsProcessed:
            if 'ppPrn' in clArgs: print( f' Processing {val}')
            cols = [ x for x in range(9) if x not in val['bCols'] ]
            for cIdx in cols:
                if canidates[val['aRow']][cIdx]!=0 and val['cVal'] in canidates[val['aRow']][cIdx]:
                    canidates[val['aRow']][cIdx].remove(val['cVal'])
                    numPruned += 1

                    if 'ppPrn' in clArgs: 
                        print('    remove {} from ({},{})'.format(val['cVal'], val['aRow'], cIdx))

    colsProcessed = []
    for val in ppColAbsCoordD.values():
        if val['aCol'] not in colsProcessed:
            if 'ppPrn' in clArgs: print( f' Processing {val}')
            rows = [ x for x in range(9) if x not in val['bRows'] ]
            for rIdx in rows:
                if canidates[rIdx][val['aCol']]!=0 and val['cVal'] in canidates[rIdx][val['aCol']]:
                    canidates[rIdx][val['aCol']].remove(val['cVal'])
                    numPruned += 1

                    if 'ppPrn' in clArgs: 
                        print('    remove {} from ({},{})'.format(val['cVal'], rIdx, val['aCol'] ))

    if 'ppPrn' in clArgs: 
        print()
        pr.printCanidates(canidates)
    ####################################################################################

    return numPruned,canidates
############################################################################
