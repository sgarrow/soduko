import fillRoutines  as fr
from itertools import combinations
import pprint as pp
import printRoutines as pr
import mapping as mp

def mapSrqsToRows(canidates): # In canidates rows are rows
    sqrsToRows = []
    squareNums = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]] 
    for squareNum in squareNums:
        rowsInSq = [ x+squareNum[0]*3 for x in [0,1,2] ]
        colsInSq = [ x+squareNum[1]*3 for x in [0,1,2] ]
        coordsInSq   = [ [r,c] for r in rowsInSq for c in colsInSq ]
        candatesSq   = [ canidates[x[0]][x[1]] for x in coordsInSq ] 
        sqrsToRows.append(candatesSq)
    return sqrsToRows
#############################################################################

def mapRowsToSqrs(canidates): # In canidates rows are squares
    rowsToSqrs = []
    squareNums = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]] 
    rowsToSqrs = [ [None]*9 for i in range(9) ]

    for ii,squareNum in enumerate(squareNums):
        currRowToMap = canidates[ii]
        rowsInSq = [ x+squareNum[0]*3 for x in [0,1,2] ]
        colsInSq = [ x+squareNum[1]*3 for x in [0,1,2] ]
    
        for ii,r in enumerate(rowsInSq):
            for jj,c in enumerate(colsInSq):
                rowsToSqrs[r][c] = currRowToMap[ii*3+jj]
    return rowsToSqrs
#############################################################################

def mapRowsToCols(canidates):
    Xpos = [[row[i] for row in canidates] for i in range(len(canidates[0]))]
    return Xpos
#############################################################################

def mapColsToRows(canidates):
    Xpos = [[row[i] for row in canidates] for i in range(len(canidates[0]))]
    return Xpos
#############################################################################

def printCanidates(canidates):
    print('   col 0  col 1  col 2   col 3  col 4  col 5   col 6  col 7  col 8  ')
    for rIdx,row in enumerate(canidates):     # for each row
        print('++------+------+------++------+------+------++------+------+------++')
        numPrintedThisRow = False
        for ii in range(3):   # print 3 lines.

            numPrintedThisLine = False
            lineToPrn = ''
            thingsToPrint = list(range( ii*3+1, ii*3+4 )) # 1,2,3; 4,5,6; 7,8,9
            #print(thingsToPrint)
            lineToPrn += '|'
            for cIdx,cell in enumerate(row):
                for num in thingsToPrint:
                    if (num-1)%3 == 0: 
                        lineToPrn += '|'
                    if cell != 0 and num in cell:
                        lineToPrn += '{:2}'.format(num)
                        numPrintedThisLine = True
                        numPrintedThisRow  = True
                    else:
                        lineToPrn += '  '
                if (cIdx+1)%3 == 0:  
                    lineToPrn += '|'
            lineToPrn += '| row {}'.format(rIdx)

            if numPrintedThisLine:
                print(lineToPrn)
            if not numPrintedThisRow and ii == 2:
                print(lineToPrn)

        if (rIdx+1)%3 ==0:
            print('++------+------+------++------+------+------++------+------+------++')
    return 0
############################################################################

def prune_PP(canidates):
    Xcanidates = mapSrqsToRows(canidates)

    printCanidates(canidates)
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
        print('square {} has row pointing pair on row {} cols {},{} (val={})'.\
            format(v['A_sqr'],r0,c0,c1,v['C_val']))
        ppD2[k] = { 'aRow':r0, 'bCols':[c0,c1], 'cVal':v['C_val'] }
    pp.pprint(ppD2)

    rowsProcessed = []
    for v in ppD2.values():
        if v['aRow'] not in rowsProcessed:
            cols = [ x for x in range(9) if x not in v['bCols'] ]
            for c in cols:
                if canidates[v['aRow']][c] != 0 and v['cVal'] in canidates[v['aRow']][c]:
                    canidates[ v['aRow']][c].remove(v['cVal'])
                    print('  removed {} from {},{}'.\
                        format(v['cVal'], v['aRow'], c))

    printCanidates(canidates)
    return 0,canidates
############################################################################


if __name__ == '__main__':
    canidates = \
    [
        [  0,    0,    0,            [2,3,7,9],[2,3,7,9],[2,7,9],       0,        0,      [2,3] ],
        [  0,    [2,9],[2,3,9],      0,        0,        0,             [2,3,9],  0,      0     ],
        [ [3,9], 0,    0,            0,        [2,3,9],  0,             0,        [2,3,9],0     ],

        [ 0,0,0,0,0,0,0,0,0],
        [ 0,0,0,0,0,0,0,0,0],
        [ 0,0,0,0,0,0,0,0,0],
        [ 0,0,0,0,0,0,0,0,0],
        [ 0,0,0,0,0,0,0,0,0],
        [ 0,0,0,0,0,0,0,0,0],
    ]

    loopNumPruned, canidates = prune_PP(canidates)


