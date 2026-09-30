import sys
import pprint        as pp

import utils         as ut
import printRoutines as pr
#############################################################################

def pruneClaimCanidates(canidates, cfgDic):
    n = 2
    numPruned = 0
    colorCordAndValDict = {}
    allBinsHeightN = ut.getAllBinsHeightN(canidates, n)

    coordsAndValsOfCanidatesWithBinsHeigtN = {}
    for row in range(9):
        for col in range(9):

            if canidates[row][col] != 0:

                for canVal in allBinsHeightN[row]:

                    if canVal in canidates[row][col]:

                        coordsAndValsOfCanidatesWithBinsHeigtN[len(coordsAndValsOfCanidatesWithBinsHeigtN)] = \
                            {'coord': [row,col], 'val': canVal}

                        colorCordAndValDict[len(colorCordAndValDict)] = \
                        {'GRN': {'coord': [row, col], 'val': canVal }}

    print()
    print(allBinsHeightN)
    print()
    pp.pprint(coordsAndValsOfCanidatesWithBinsHeigtN)
    print()
    pr.printCanidates(canidates, colorCordAndValDict)
    print()

    #sys.exit()
    return numPruned,canidates
#############################################################################
