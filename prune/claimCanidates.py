import sys
import copy          as cp
import pprint        as pp

import utils         as ut
import printRoutines as pr
#############################################################################
def sameSqr(inLst):
    if len(inLst) == len(set(inLst)):
        # All elements are unique
        pass
    else:
        return False

    mod3 = [ x//3 for x in inLst ]
    if len(set(mod3)) == 1:
        # same block
        return True
    else:
        # not same block
        return False
#############################################################################

def pruneClaimCanidates(canidates, house, cfgDic):
    cpyDic = {'row':cp.deepcopy, 'col':ut.mapColsToRows, 'sqr':ut.mapSrqsToRows}
    xCanidates = cpyDic[house](canidates)

    numPruned = 0
    colorCordAndValDict = {} # Initialze color Dict.

    # Find all bins height 2 or 3, combine them, find the coords and vals
    # and put that info in coordValsOfAllCansWithBinsHeight23 which is the
    # pertinantent output of this section of code.  Also use this info to
    # build a color coded canidates DB.  Printing the canidates at this point
    # shows all the canidates that appear 2 or three times in a given row but
    # those 2 or 3 canidates might not be in the same square.
    allBinsHeight2 = ut.getAllBinsHeightN(xCanidates, 2)
    allBinsHeight3 = ut.getAllBinsHeightN(xCanidates, 3)
    allBinsHeight23 = [ a+b for a,b in zip(allBinsHeight2,allBinsHeight3)]

    coordValsOfAllCansWithBinsHeight23 = {}
    ii = 0
    for row in range(9):
        for col in range(9):
            if xCanidates[row][col] != 0:
                for canVal in allBinsHeight23[row]:
                    if canVal in xCanidates[row][col]:

                        coordValsOfAllCansWithBinsHeight23[ii] = \
                            {'coord': [row,col], 'val': canVal}

                        colorCordAndValDict[len(colorCordAndValDict)] = \
                        {'GRN': {'coord': [row, col], 'val': canVal }}

                        ii += 1

    #print()
    #print(allBinsHeight2)
    #print(allBinsHeight3)
    #print(allBinsHeight23)
    #pp.pprint(coordValsOfAllCansWithBinsHeight23)
    #pr.printCanidates(canidates, colorCordAndValDict)
    ###################################################

    # Build a new dict, prunnedRowDict, which is the pertinent output of this
    # section of code, that contains ONLY the 2,3 values that are in the
    # same sqr. Printing the canidates at this point shows all the canidates 
    # that appear 2 or 3 times in a given row and are in the same square.
    rowDicts = {}
    for v in coordValsOfAllCansWithBinsHeight23.values():
        currKey = ( v['coord'][0], v['val'] )

        if currKey not in rowDicts:
            rowDicts[currKey] = [     v[ 'coord' ][1]   ]
        else:
            rowDicts[currKey].append( v[ 'coord' ][1] )
    prunnedRowDict = { k:v for k,v in rowDicts.items() if sameSqr(v) }

    colorCordAndValDict = {} # Reinitialze color Dict.
    for k,v in prunnedRowDict.items():
        for col in v:
            colorCordAndValDict[len(colorCordAndValDict)] = \
            {'GRN': {'coord': [ k[0], col ], 'val': k[1] }}

    #print()
    #pp.pprint(rowDicts)
    #pp.pprint(prunnedRowDict)
    #pr.printCanidates(canidates, colorCordAndValDict)
    ###################################################

    # Color code in RED all the things that can be removed per the things 
    # that are colored green.
    for k,v in prunnedRowDict.items():
        currSqrRows, currSqrCols = ut.findRowsColsInSquare(k[0], v[0])
        currSqrRows.remove(k[0])
        valToRemove = k[1]
        for currRow in currSqrRows:
            for currCol in currSqrCols:
                #print('currRow,currCol,valToRemove',currRow,currCol,valToRemove)
                #print(xCanidates[currRow][currCol])
                #print()
                if xCanidates[currRow][currCol] != 0 and \
                   valToRemove in xCanidates[currRow][currCol]:

                    colorCordAndValDict[len(colorCordAndValDict)] = \
                    {'RED': {'coord': [currRow, currCol], 'val': valToRemove}}
    #print()
    #pr.printCanidates(xCanidates, colorCordAndValDict)
    ###################################################

    if cfgDic['cc']['prnLevel'] >= 3:
        pr.printCanidates(xCanidates, colorCordAndValDict)

    # Now remove (prune) all the things that are colored red.
    removeStr = ''
    for k,v in prunnedRowDict.items():
        currSqrRows, currSqrCols = ut.findRowsColsInSquare(k[0], v[0])
        currSqrRows.remove(k[0])
        valToRemove = k[1]
        for currRow in currSqrRows:
            for currCol in currSqrCols:
                if xCanidates[currRow][currCol] != 0 and \
                   valToRemove in xCanidates[currRow][currCol]:
                    xCanidates[currRow][currCol].remove(valToRemove)
                    numPruned += 1
                    removeStr += '       remove {} from ({},{})\n'.\
                        format(currRow,currCol,valToRemove)

    if cfgDic['cc']['prnLevel'] >= 2:
        print(removeStr, end = '')

    cpyDic = {'row':cp.deepcopy, 'col':ut.mapRowsToCols, 'sqr':ut.mapRowsToSqrs}
    canidates = cpyDic[house](xCanidates)

    return numPruned,canidates
#############################################################################
