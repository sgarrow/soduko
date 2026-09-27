from itertools import combinations
import copy          as cp
import pprint        as pp

import printRoutines as pr
import utils         as ut
#############################################################################

def pruneXwings(canidates, house, cfgDic):
    cpyDic = {'row':cp.deepcopy, 'col':ut.mapColsToRows, 'sqr':ut.mapSrqsToRows}
    xCanidates = cpyDic[house](canidates)

    binsHeight2 = ut.getAllBinsHeightTwo(xCanidates)
    numPruned   = 0
    colorDict   = {}
    xWingD      = {}
    myD         = {}

    for idx,lstOfVals in enumerate(binsHeight2):
        for val in lstOfVals:
            cols = [ c for c,lst in enumerate(xCanidates[idx]) if lst != 0 and val in lst ]
            #print(' in row {}, {} appears exactly twice - cols {}'.format(idx, val, cols))
            myD[len(myD)] = { 'A_row':idx, 'B_cols':cols, 'C_val':val,  }

    combSet = combinations(myD.values(), 2)

    for comb in combSet:
        #print(comb)
        if comb[0]['C_val'] == comb[1]['C_val'] and comb[0]['B_cols'] == comb[1]['B_cols']:

            xWingD[len(xWingD)] = \
                { 'A_rows': [ comb[0]['A_row'], comb[1]['A_row'] ],
                  'B_cols':   comb[0]['B_cols'],
                  'C_val' :   comb[0]['C_val']  }

    for xWing in xWingD.values():

        if cfgDic['xw']['prnLevel'] >= 2:
            print(xWing)

        for row in xWing['A_rows']:
            for col in xWing['B_cols']:

                colorDict[len(colorDict)] = \
                    {'GRN': {'coord': [row, col], 'val': xWing['C_val']}}

        for row in range( 8 ):
            for col in xWing['B_cols']:
                if (xCanidates[row][col] != 0)  and \
                    row not in xWing['A_rows']  and \
                    (xWing['C_val'] in xCanidates[row][col]):

                    colorDict[len(colorDict)] = \
                        {'RED': {'coord': [row, col], 'val': xWing['C_val']}}

    if len(xWingD) > 0:
        if cfgDic['xw']['prnLevel'] >= 2:
            pr.printCanidates(xCanidates, colorDict)

    for xWing in xWingD.values():
        for row in range( 8 ):
            for col in xWing['B_cols']:
                if (xCanidates[row][col] != 0)  and \
                    row not in xWing['A_rows']  and \
                    (xWing['C_val'] in xCanidates[row][col]):

                    if cfgDic['xw']['prnLevel'] >= 2:
                        print('      remove {} from ({},{})'.format(xWing['C_val'], row, col))

                    xCanidates[row][col].remove(xWing['C_val'])
                    numPruned += 1

    cpyDic = {'row':cp.deepcopy, 'col':ut.mapRowsToCols, 'sqr':ut.mapRowsToSqrs}
    canidates = cpyDic[house](xCanidates)

    return(numPruned, canidates)
############################################################################
