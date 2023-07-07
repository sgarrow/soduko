import printRoutines as pr
#############################################################################

def findRowsColsInSquare(rIdx, cIdx):
    if rIdx % 3 == 0: rOffsets = [ 1, 2]
    if rIdx % 3 == 1: rOffsets = [-1, 1]
    if rIdx % 3 == 2: rOffsets = [-1,-2] 
    if cIdx % 3 == 0: cOffsets = [ 1, 2]
    if cIdx % 3 == 1: cOffsets = [-1, 1] 
    if cIdx % 3 == 2: cOffsets = [-1,-2] 
    rowsInSquare = [ rIdx+rOffsets[0], rIdx+rOffsets[1] ]
    colsInSquare = [ cIdx+cOffsets[0], cIdx+cOffsets[1] ]
    return rowsInSquare, colsInSquare
#############################################################################

def buildColDupsLst(canidates):
    # Make a list containing info on naked pairs in each row.
    # e.g., if row 2 contains 2 naked pairs then rowDups could look like:
    # [ [], [], [[3,7],[5,9]], [], [], [], [], [], [] ]
    Xpos = [[row[i] for row in canidates] for i in range(len(canidates[0]))]
    colDups = []
    for cIdx,col in enumerate(Xpos):
        dup1 = [ el for ii, el in enumerate(col) if el in col[:ii] ]
        dupNo0 = [ x for x in dup1 if x !=0 ]
        dupNo0Len2 = [x for x in dupNo0 if len(x)==2]
        colDups.append(dupNo0Len2)

    # Now add the rows where the pairs exist.  Then it might look like this:
    # [ [], [],  [ [[3,7],[1,4]],[[5,9],[6,7] ],  [], [], [], [], [], [] ]
    # Read: In the canidates list, 
    # Col 2, rows 1 and 4 is [3,7] and Col 2, rows 6 and 7 is [5,9]
    for cIdx,currListOfDupPairs in enumerate(colDups):
        if currListOfDupPairs != []:
            for idxOfCurrDupPair, currDupPair in enumerate(currListOfDupPairs):
                rowsOfThisDupPair = \
                [row for row,el in enumerate(Xpos[cIdx]) if el==currDupPair]
                colDups[cIdx][idxOfCurrDupPair] = \
                [currDupPair,rowsOfThisDupPair]
    return colDups
#############################################################################

def buildRowDupsLst(canidates):
    # Make a list containing info on naked pairs in each row.
    # e.g., if row 2 contains 2 naked pairs then rowDups could look like:
    # [ [], [], [[3,7],[5,9]], [], [], [], [], [], [] ]

    rowDups = []
    for rIdx,row in enumerate(canidates):
        dup1 = [ el for ii, el in enumerate(row) if el in row[:ii] ]
        dupNo0 = [ x for x in dup1 if x !=0 ]
        dupNo0Len2 = [x for x in dupNo0 if len(x)==2]
        rowDups.append(dupNo0Len2)

    # Now add the cols where the pairs exist.  Then it might look like this:
    # [ [], [],  [ [[3,7],[1,4]],[[5,9],[6,7] ],  [], [], [], [], [], [] ]
    # Read: In the canidates list, 
    # Row 2, cols 1 and 4 is [3,7] and Row 2, cols 6 and 7 is [5,9]
    for rIdx,currListOfDupPairs in enumerate(rowDups):
        if currListOfDupPairs != []:
            for idxOfCurrDupPair, currDupPair in enumerate(currListOfDupPairs):
                colsOfThisDupPair = \
                [col for col,el in enumerate(canidates[rIdx]) if el==currDupPair]
                rowDups[rIdx][idxOfCurrDupPair] = \
                [currDupPair,colsOfThisDupPair]
    return rowDups
#############################################################################

def buildSqrDupsLst(canidates):

    sqrDups = []
    squareNums = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]] 

    for squareNum in squareNums:
        rowsInSq = [ x+squareNum[0]*3 for x in [0,1,2] ]
        colsInSq = [ x+squareNum[1]*3 for x in [0,1,2] ]

        coordsInSq     = [ [r,c] for r in rowsInSq for c in colsInSq ]
        candatesSq     = [ canidates[x[0]][x[1]] for x in coordsInSq ] 
        candatesLen2   = [ x for x in candatesSq if x != 0 and len(x)==2]
        canLen2Appear2 = [ x for x in candatesLen2 if candatesLen2.count(x) == 2 ]
        canL2A2NoDup   = []
        [canL2A2NoDup.append(x) for x in canLen2Appear2 if x not in canL2A2NoDup ]

        sqrDups.append(canL2A2NoDup)

    return sqrDups
#############################################################################
def pruneNakedPairs(canidates):

    print('\nPruning canidates')
    # Print canidates before pruning wrt naked pairs.
    #print('before pruning')
    #pr.prettyPrint3DArray(canidates)

    ####################################################################
    # Make a list containing info on naked pairs in each row and col.
    print('  Finding naked canidate pairs in rows and cols.')
    rowDups = buildRowDupsLst(canidates)
    #pr.printRowDupsLst(rowDups)
    #print()
    numPruned = 0
    print('\n  Pruning wrt rows')
    for rIdx,currListOfDupPairs in enumerate(rowDups):
        if currListOfDupPairs != []:
            for idxOfCurrDupPair,currDupPairAndCoord in enumerate(currListOfDupPairs):
                for ii in range(2):                           # 1st item is the pair, 2nd item is the cols its in.
                    print( '  Removing {} from all cols in row {} except for cols {} and {}'.
                        format(currDupPairAndCoord[0][ii], rIdx, currDupPairAndCoord[1][0],currDupPairAndCoord[1][1] ))
                    for jj in range(9):                       # Remove the value from all the cols except
                        if jj not in currDupPairAndCoord[1]:  # don't remove it from the cols where the dup itself lives.
                            try:                              # Can't remove it if it's not there.
                                canidates[rIdx][jj].remove(currDupPairAndCoord[0][ii])
                                print('   Removing {} from [{},{}]'.format(currDupPairAndCoord[0][ii], rIdx, jj ))
                                numPruned += 1
                            except:
                                pass
    print('  numPruned = {}.\n'.format(numPruned))
    #pr.prettyPrint3DArray(canidates)

    print('  Pruning wrt squares (based on row dups)')
    for rIdx,currListOfDupPairs in enumerate(rowDups):
        if currListOfDupPairs != []:
            for idxOfCurrDupPair,currDupPairAndCoord in enumerate(currListOfDupPairs):
                for ii in range(2):                           # 1st item is the pair, 2nd item is the cols its in.
                    inSameSquare = ( currDupPairAndCoord[1][0]//3 == currDupPairAndCoord[1][1]//3 )
                    print( '  Pair {} is in cols {} of row {}. In same square = {}.'.\
                        format(currDupPairAndCoord[0], currDupPairAndCoord[1], rIdx, inSameSquare ) )

                    if inSameSquare:

                        print( '  Removing {} and {} from all cells in square containing cells [{},{}] and [{},{}]. '.\
                            format(currDupPairAndCoord[0][0], currDupPairAndCoord[0][1],
                                   rIdx, currDupPairAndCoord[1][0], rIdx, currDupPairAndCoord[1][1] ) )

                        for cIdx in currDupPairAndCoord[1]:

                            rowsInSquare, colsInSquare = findRowsColsInSquare(rIdx, cIdx)

                            for r in rowsInSquare:
                                for c in colsInSquare:
                                    for ii in range(9):
                                        if r != rIdx and c != cIdx:
                                            try:                              # Can't remove it if it's not there.
                                                canidates[r][c].remove(currDupPairAndCoord[0][ii])
                                                print('    Removing {} from [{},{}]'.format(currDupPairAndCoord[0][ii], r, c ))
                                                numPruned += 1
                                            except:
                                                pass

    print('  numPruned = {}.\n'.format(numPruned))
    #pr.prettyPrint3DArray(canidates)
    ####################################################################

    colDups = buildColDupsLst(canidates)
    #pr.printColDupsLst(colDups)
    #print()

    print('  Pruning wrt cols')
    for cIdx,currListOfDupPairs in enumerate(colDups):
        if currListOfDupPairs != []:
            for idxOfCurrDupPair,currDupPairAndCoord in enumerate(currListOfDupPairs):
                for ii in range(2):                           # 1st item is the pair, 2nd item is the cols its in.
                    print( '  Removing {} from all rows in col {} except for rows {} and {}'.
                        format(currDupPairAndCoord[0][ii], cIdx, currDupPairAndCoord[1][0],currDupPairAndCoord[1][1] ))
                    for jj in range(9):                       # Remove the value from all the cols except
                        if jj not in currDupPairAndCoord[1]:  # don't remove it from the cols where the dup itself lives.
                            try:                              # Can't remove it if it's not there.
                                canidates[jj][cIdx].remove(currDupPairAndCoord[0][ii])
                                print('   Removing {} from [{},{}]'.format(currDupPairAndCoord[0][ii], jj, cIdx ))
                                numPruned += 1
                            except:
                                pass
    print('  numPruned = {}.\n'.format(numPruned))
    #pr.prettyPrint3DArray(canidates)

    print('  Pruning wrt squares (based on col dups)')
    for cIdx,currListOfDupPairs in enumerate(colDups):
        if currListOfDupPairs != []:
            for idxOfCurrDupPair,currDupPairAndCoord in enumerate(currListOfDupPairs):
                for ii in range(2):                           # 1st item is the pair, 2nd item is the cols its in.
                    inSameSquare = ( currDupPairAndCoord[1][0]//3 == currDupPairAndCoord[1][1]//3 )
                    print( '  Pair {} is in rows {} of col {}. In same square = {}.'.\
                        format(currDupPairAndCoord[0], currDupPairAndCoord[1], cIdx, inSameSquare ) )

                    if inSameSquare:

                        print( '  Removing {} and {} from all cells in square containing cells [{},{}] and [{},{}]. '.\
                            format(currDupPairAndCoord[0][0], currDupPairAndCoord[0][1],
                                   currDupPairAndCoord[1][0], cIdx, currDupPairAndCoord[1][1], cIdx ) )

                        for rIdx in currDupPairAndCoord[1]:

                            rowsInSquare, colsInSquare = findRowsColsInSquare(rIdx, cIdx)

                            for r in rowsInSquare:
                                for c in colsInSquare:
                                    for ii in range(9):
                                        if r != rIdx and c != cIdx:
                                            try:                              # Can't remove it if it's not there.
                                                canidates[r][c].remove(currDupPairAndCoord[0][ii])
                                                print('    Removing {} from [{},{}]'.format(currDupPairAndCoord[0][ii], r, c ))
                                                numPruned += 1
                                            except:
                                                pass

    print('  numPruned = {}.\n'.format(numPruned))
    #pr.prettyPrint3DArray(canidates)
    ####################################################################

    sqrDups = buildSqrDupsLst(canidates)
    pr.printSqrDupsLst(sqrDups)
    print()
    print('  Pruning wrt squares.' )

    squareCoords = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]] 

    for ii,squareCoord in enumerate(squareCoords):
        rowsInSq = [ x+squareCoord[0]*3 for x in [0,1,2] ]
        colsInSq = [ x+squareCoord[1]*3 for x in [0,1,2] ]

        for r in rowsInSq:
            for c in colsInSq:
                for currDup in sqrDups[ii]:
                    if canidates[r][c] != currDup:
                        for val in currDup:
                            try:
                                canidates[r][c].remove(val)
                                print('    Removing {} from [{},{}]'.format(val, r, c ))
                                numPruned += 1
                            except:
                                pass

    print('  numPruned = {}.\n'.format(numPruned))
    #pr.prettyPrint3DArray(canidates)
    return(numPruned, canidates)
#############################################################################

