from itertools import combinations
import copy          as cp
import mapping       as mp
#############################################################################

def flatten(inLst):
    outLst = []
    for elem in inLst:
        try:
            for subEl in elem:
                outLst.append(subEl)
        except TypeError:
            outLst.append(elem)
    return outLst
#############################################################################

def genHistogram(inLst):
    hist = []
    for histBin in range(min(inLst), max(inLst)+1):
        binHeight = len([1 for x in inLst if x==histBin])
        if binHeight > 0:
            hist.append((histBin, binHeight))
    return hist
#############################################################################

def pruneXwings(canidates, house, lclPrintDic):
    cpyDic = {'row':cp.deepcopy, 'col':mp.mapColsToRows, 'sqr':mp.mapSrqsToRows}
    xCanidates = cpyDic[house](canidates)

    numPruned = 0

    allBinsHeightTwo = []
    for row in xCanidates:
        flatRow = flatten(row)
        histRow = genHistogram(flatRow)
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
    if lclPrintDic['xwPrn'] >= 1:
        for k,v in xWingD.items():
            myDstr = pp.pformat(v)
            print('\n    {} {}'.format(house, myDstr), end = '')
        print()

    alreadyPrinted = False
    for xWing in xWingD.values():
        for rIdx,row in enumerate(xCanidates):
            for cIdx in xWing['B_cols']:
                if (rIdx not in xWing['A_rows'])  and \
                    (row[cIdx] != 0) and \
                    (xWing['C_val'] in row[cIdx]):
                    xCanidates[rIdx][cIdx].remove(xWing['C_val'])
                    numPruned += 1

                    if lclPrintDic['xwPrn'] >= 2:
                        pr.printCanidates(xCanidates, alreadyPrn = alreadyPrinted)
                        #print({True: '', False: '   {}'.format(xWing)} [alreadyPrinted])
                        alreadyPrinted = True

                    if lclPrintDic['xwPrn'] >= 1:
                        print('      remove {} from ({},{})'.format(xWing['C_val'], rIdx, cIdx))

    cpyDic = {'row':cp.deepcopy, 'col':mp.mapRowsToCols, 'sqr':mp.mapRowsToSqrs}
    canidates = cpyDic[house](xCanidates)

    return(numPruned, canidates)
############################################################################
