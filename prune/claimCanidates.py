import sys
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

def pruneClaimCanidates(canidates, cfgDic):
    numPruned = 0
    colorCordAndValDict = {}

    allBinsHeight2 = ut.getAllBinsHeightN(canidates, 2)
    allBinsHeight3 = ut.getAllBinsHeightN(canidates, 3)
    allBinsHeight23 = [ a+b for a,b in zip(allBinsHeight2,allBinsHeight3)]

    coordValsOfAllCansWithBinsHeight23 = {}
    ii = 0
    for row in range(9):
        for col in range(9):

            if canidates[row][col] != 0:

                for canVal in allBinsHeight23[row]:

                    if canVal in canidates[row][col]:

                        coordValsOfAllCansWithBinsHeight23[ii] = \
                            {'coord': [row,col], 'val': canVal}

                        colorCordAndValDict[len(colorCordAndValDict)] = \
                        {'GRN': {'coord': [row, col], 'val': canVal }}

                        ii += 1

    rowDicts = {}
    for v in coordValsOfAllCansWithBinsHeight23.values():
        currKey = ( v['coord'][0], v['val'] )

        if currKey not in rowDicts:
            rowDicts[currKey] = [     v[ 'coord' ][1]   ]
        else:
            rowDicts[currKey].append( v[ 'coord' ][1] )

    prunnedRowDict = { k:v for k,v in rowDicts.items() if sameSqr(v) }

    print(allBinsHeight2)
    print(allBinsHeight3)
    print(allBinsHeight23)
    pp.pprint(coordValsOfAllCansWithBinsHeight23)
    pp.pprint(rowDicts)
    print()
    pp.pprint(prunnedRowDict)
    print()
    pr.printCanidates(canidates, colorCordAndValDict)

    colorCordAndValDict = {}
    for k,v in prunnedRowDict.items():
        for col in v:
            colorCordAndValDict[len(colorCordAndValDict)] = \
            {'GRN': {'coord': [ k[0], col ], 'val': k[1] }}

    pr.printCanidates(canidates, colorCordAndValDict)
    #sys.exit()

    return numPruned,canidates
#############################################################################
