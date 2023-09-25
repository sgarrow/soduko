def mapSrqsToRows(canidates): # In canidates rows are rows
    sqrsToRows = []
    squareNums = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
    for squareNum in squareNums:
        rowsInSq = [ x+squareNum[0]*3 for x in [0,1,2] ]
        colsInSq = [ x+squareNum[1]*3 for x in [0,1,2] ]
        coordsInSq   = [ [row,col] for row in rowsInSq for col in colsInSq ]
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

        for ii,row in enumerate(rowsInSq):
            for jj,col in enumerate(colsInSq):
                rowsToSqrs[row][col] = currRowToMap[ii*3+jj]
    return rowsToSqrs
#############################################################################

def mapRowsToCols(canidates):
    xPos = [[row[i] for row in canidates] for i in range(len(canidates[0]))]
    return xPos
#############################################################################

def mapColsToRows(canidates):
    xPos = [[row[i] for row in canidates] for i in range(len(canidates[0]))]
    return xPos
#############################################################################

def getRowColFromSqrOffset(sqr,ofst):
    row              = ( ofst // 3 ) + ( (sqr // 3) * 3 )
    ofst1stCellInRow = ( row  * 9 ) + ( (sqr %  3) * 3 )
    offsetInto9X9   = ofst1stCellInRow + ofst %  3
    col = offsetInto9X9  % 9
    return row,col
