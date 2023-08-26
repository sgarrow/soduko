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

def getRowColFromSqrOffset(s,o):
    row              = ( o // 3 ) + ( (s // 3) * 3 )
    ofst1stCellInRow = ( row  * 9 ) + ( (s %  3) * 3 )
    offsetInto_9x9   = ofst1stCellInRow + o %  3
    col = offsetInto_9x9  % 9
    return row,col
