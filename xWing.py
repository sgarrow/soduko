import printRoutines as pr
import pprint as pp
import fillRoutines  as fr
from itertools import combinations

def mapRowsToCols(canidates):
    Xpos = [[row[i] for row in canidates] for i in range(len(canidates[0]))]
    return Xpos
#############################################################################

def mapColsToRows(canidates):
    Xpos = [[row[i] for row in canidates] for i in range(len(canidates[0]))]
    return Xpos
#############################################################################

def pruneXwings(canidates, house):
    #pr.printCanidates(canidates)
    import copy
    if   house == 'row':  Xcanidates = copy.deepcopy(canidates)
    elif house == 'col':  Xcanidates = mapColsToRows(canidates) 

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
    elif house == 'col':  canidates = mapRowsToCols(Xcanidates) 
    #print(house)

    return(numPruned, canidates)


