import pprint        as pp

import utils         as ut
import printRoutines as pr
#############################################################################

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

def prunePointingPairs(canidates, house, lclPrintDic):
    xCanidates = ut.mapSrqsToRows(canidates)
    numPruned  = 0

    # find all nums in rows of xCanidates (sqrs of canidates) that appear exactly twice
    allBinsHeightTwo = ut.getAllBinsHeightTwo(xCanidates)

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
    rqmt = None
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
    ppD = None
    if house == 'row': ppD = ppRowD
    if house == 'col': ppD = ppColD
    for val in ppD.values():
        row0,col0= ut.getRowColFromSqrOffset(val['A_sqr'],val['B_idxs'][0])
        row1,col1= ut.getRowColFromSqrOffset(val['A_sqr'],val['B_idxs'][1])
        if house == 'row': ppRowAbsCoordD[k]= {'aRow':row0,'bCols':[col0,col1],'cVal':val['C_val']}
        if house == 'col': ppColAbsCoordD[k]= {'aCol':col0,'bRows':[row0,row1],'cVal':val['C_val']}
        k += 1
    ####################################################################################

    # debug prints
    if lclPrintDic['ppPrn'] >= 3:
        thingsPprint = { #'allBinsHeightTwo':allBinsHeightTwo,
                         'allBinsHeightTwoD':allBinsHeightTwoD,
                         'ppRowD':ppRowD,
                         'ppColD':ppColD,
                         'ppRowAbsCoordD':ppRowAbsCoordD,
                         'ppColAbsCoordD':ppColAbsCoordD 
                         }

        for k,v in thingsPprint.items():
            myStr = ''
            print('     {} ({})'.format(k, house))
            for ii in range(len(v)):
                myStr = pp.pformat(v[ii])
                print('    ',myStr)
            print()

    ####################################################################################

    # perform associated removals Note only one of the 2 dicts looped through below will
    # have anything in it.
    alreadyPrinted = False
    rowsProcessed = []
    for val in ppRowAbsCoordD.values():
        if val['aRow'] not in rowsProcessed:
            if lclPrintDic['ppPrn'] >= 1: print( f'     Processing {val}')
            cols = [ x for x in range(9) if x not in val['bCols'] ]
            for cIdx in cols:
                if canidates[val['aRow']][cIdx]!=0 and val['cVal'] in canidates[val['aRow']][cIdx]:

                    if lclPrintDic['ppPrn'] >= 2:
                        pr.printCanidates(canidates, alreadyPrn = alreadyPrinted)
                        alreadyPrinted = True

                    canidates[val['aRow']][cIdx].remove(val['cVal'])
                    numPruned += 1

                    if lclPrintDic['ppPrn'] >= 1:
                        print('       remove {} from ({},{})'.format(val['cVal'],val['aRow'],cIdx))

    alreadyPrinted = False
    colsProcessed = []
    for val in ppColAbsCoordD.values():
        if val['aCol'] not in colsProcessed:
            if lclPrintDic['ppPrn'] >= 1: print( f'     Processing {val}')
            rows = [ x for x in range(9) if x not in val['bRows'] ]
            for rIdx in rows:
                if canidates[rIdx][val['aCol']]!=0 and val['cVal'] in canidates[rIdx][val['aCol']]:

                    if lclPrintDic['ppPrn'] >= 2:
                        pr.printCanidates(canidates, alreadyPrn = alreadyPrinted)
                        alreadyPrinted = True

                    canidates[rIdx][val['aCol']].remove(val['cVal'])
                    numPruned += 1

                    if lclPrintDic['ppPrn'] >= 1:
                        print('       remove {} from ({},{})'.format(val['cVal'],rIdx,val['aCol']))
    ####################################################################################

    return numPruned,canidates
############################################################################
