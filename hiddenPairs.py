import pprint        as pp
import fillRoutines  as fr
import printRoutines as pr
#############################################################################

def printRowHiddenPairsDict(rhpd):
    if rhpd == {}:
        print( '   No row hidden pairs found') 
        return
    for k,v in rhpd.items():
        print('   Row {} has hidden pair {} in cols {}'.\
            format(rhpd[k]['row'], rhpd[k]['vals'], rhpd[k]['cols']))
    return
#############################################################################

def printColHiddenPairsDict(chpd):
    if chpd == {}:
        print( '   No col hidden pairs found') 
        return
    for k,v in chpd.items():
        print('   Col {} has hidden pair {} in rows {}'.\
            format(chpd[k]['col'], chpd[k]['vals'], chpd[k]['rows']))
    return
#############################################################################

def printSqrHiddenPairsDict(shpd):
    if shpd == {}:
        print( '   No sqr hidden pairs found') 
        return
    for k,v in shpd.items():
        print('   Sqr {} has hidden pair {} at indeces {}'.\
            format(shpd[k]['sqr'], shpd[k]['vals'], shpd[k]['idx']))
    return
#############################################################################

def buildRowHiddenPairDict(canidates):  # Finds hidden and naked pairs also finds naked triplets when N=3.

    #pr.prettyPrint3DArray(canidates)
    N = 2
    binsHeight_N_ThisRow = []
    binsHeight_N_AllRows = []
    for rIdx,row in enumerate(canidates):
        flatRow = fr.flatten(row)
        rowHist = fr.genHistogram(flatRow)
        binsHeight_N_ThisRow = [ x[0] for x in rowHist if 1 < x[1] < N+1 and x[0] != 0 ]
        binsHeight_N_AllRows.append(binsHeight_N_ThisRow)
    #print('\nvalues that appear exactly {} times on a given row'.format(N))
    #pp.pprint(binsHeight_N_AllRows)

    lstOf_N_Dict = []
    for rIdx,binHeight_N_Row in enumerate(binsHeight_N_AllRows):
        myDict = {}
        for val in binHeight_N_Row:
            myDict[val] = [cIdx for cIdx, x in enumerate(canidates[rIdx]) if x != 0 and val in canidates[rIdx][cIdx]]
        lstOf_N_Dict.append(myDict)
    #print('\nvalueThatApearsExactlyN : theColsWhereTheyAppear (on a given row)')
    #pp.pprint(lstOf_N_Dict)

    itemNum = 0
    hidden_N_Dict = {}
    for rIdx,aDict in enumerate(lstOf_N_Dict):
        aDictValues = list(aDict.values()) # values are the cols
        #print(  '  aDict.values() ', aDict.values())
        for val in aDictValues:
            theCount = aDictValues.count(val)
            if theCount == N:
                keysOfThisVal = [ k for k,v in aDict.items() if v == val ] # keys are the vals
                if { 'row' : rIdx, 'cols' : val, 'vals' : keysOfThisVal } not in hidden_N_Dict.values():
                    hidden_N_Dict[itemNum] = { 'row' : rIdx, 'cols' : val, 'vals' : keysOfThisVal }
                    itemNum += 1
    #print('\nhidden_N_Dict')
    #pp.pprint(hidden_N_Dict)
    #print()
    return(hidden_N_Dict)
#############################################################################

def buildColHiddenPairDict(canidates):
    Xpos = [[row[i] for row in canidates] for i in range(len(canidates[0]))]
    binsHeightTwoThisCol = []
    binsHeightTwoAllCols = []
    for cIdx,col in enumerate(Xpos):
        flatCol = fr.flatten(col)
        colHist = fr.genHistogram(flatCol)
        binsHeightTwoThisCol = [ x[0] for x in colHist if x[1] == 2 and x[0] != 0 ]
        binsHeightTwoAllCols.append(binsHeightTwoThisCol)
    #print('\nvalues that appear exactly twice on a given col')
    #pp.pprint(binsHeightTwoAllCols)

    lstOfDict = []
    for cIdx,binHeight2Col in enumerate(binsHeightTwoAllCols):
        myDict = {}
        for val in binHeight2Col:
            myDict[val] = [rIdx for rIdx, x in enumerate(Xpos[cIdx]) if x != 0 and val in canidates[rIdx][cIdx]]
        lstOfDict.append(myDict)
    #print('\nvalueThatApearsExactlyTwice : theRowsWhereTheyAppear (on a given col)')
    #pp.pprint(lstOfDict)
    
    itemNum = 0
    hiddenPairsDict = {}
    for cIdx,aDict in enumerate(lstOfDict):
        aDictValues = list(aDict.values()) # values are the rows
        #print(  'aDict.values()', aDict.values())
        for val in aDictValues:
            theCount = aDictValues.count(val)
            if theCount == 2:
                keysOfThisVal = [ k for k,v in aDict.items() if v == val ] # keys are the vals
                hiddenPairsDict[itemNum] = { 'col' : cIdx, 'rows' : val, 'vals' : keysOfThisVal }
                itemNum += 1
    #print('\nhiddenPairsDict')
    #pp.pprint(hiddenPairsDict)
    
    itemNum = 0
    hiddenPairsDict2 = {}
    for key,value in hiddenPairsDict.items():
        if value not in hiddenPairsDict2.values():
            hiddenPairsDict2[itemNum] = value
            itemNum += 1
    #print('\nhiddenPairsDict2 cols')
    #pp.pprint(hiddenPairsDict2)
    
    return(hiddenPairsDict2)
#############################################################################
def buildSqrHiddenPairDict(canidates):

    #pr.prettyPrint3DArray(canidates)
    squareCoords = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]] 
    binsHeightTwoAllSqrs = []
    canidatesAllSqr = []
    for squareCoord in squareCoords:
        rowsInSqr    = [ x+squareCoord[0]*3 for x in [0,1,2] ]
        colsInSqr    = [ x+squareCoord[1]*3 for x in [0,1,2] ]
        coordsInSqr  = [ [r,c] for r in rowsInSqr for c in colsInSqr ]
        canidatesSqr = [ canidates[x[0]][x[1]] for x in coordsInSqr ]
    
        binsHeightTwoThisSqr = []
        flatSqr = fr.flatten(canidatesSqr)
        sqrHist = fr.genHistogram(flatSqr)
        binsHeightTwoThisSqr = [ x[0] for x in sqrHist if x[1] == 2 and x[0] != 0 ]
        binsHeightTwoAllSqrs.append(binsHeightTwoThisSqr)

        canidatesAllSqr.append(canidatesSqr)

    #print()
    #print('\n canidatesAllSqr')
    #pp.pprint(canidatesAllSqr)
    #print()
    #print('\nbinsHeightTwoAllSqrs: values that appear exactly twice in a given square')
    #pp.pprint(binsHeightTwoAllSqrs)


    lstOfDict = []
    for sIdx,binHeight2Sqr in enumerate(binsHeightTwoAllSqrs):
        myDict = {}
        for val in binHeight2Sqr:
            myDict[val] = [idx for idx,x in enumerate(canidatesAllSqr[sIdx]) if x != 0 and val in canidatesAllSqr[sIdx][idx] ]
        lstOfDict.append(myDict)
    #print('\nvalueThatApearsExactlyTwice : theIndexWhereTheyAppear (on a given square)')
    #pp.pprint(lstOfDict)

    itemNum = 0
    hiddenPairsDict = {}
    for sIdx,aDict in enumerate(lstOfDict):
        aDictValues = list(aDict.values()) # values are the index in the square 1-9
        #print(  'aDict.values()', aDict.values())
        for val in aDictValues:
            theCount = aDictValues.count(val)
            if theCount == 2:
                keysOfThisVal = [ k for k,v in aDict.items() if v == val ] # keys are the vals
                hiddenPairsDict[itemNum] = { 'sqr' : sIdx, 'idx' : val, 'vals' : keysOfThisVal }
                itemNum += 1
    #print('\nhiddenPairsDict')
    #pp.pprint(hiddenPairsDict)

    itemNum = 0
    hiddenPairsDict2 = {}
    for key,value in hiddenPairsDict.items():
        if value not in hiddenPairsDict2.values():
            hiddenPairsDict2[itemNum] = value
            itemNum += 1
    #print('\nhiddenPairsDict2 sqr')
    #pp.pprint(hiddenPairsDict2)

    #pr.prettyPrint3DArray(canidates)
    return(hiddenPairsDict2)
#############################################################################

def pruneHiddenPairs(canidates):

    print('\nPrunng hidden pairs ************************************ Start')
    #pr.prettyPrint3DArray(canidates)
    numPruned = 0

    ####################################################################
    # Make a dict containing info on hidden pairs in each row.
    print('  Finding hidden pairs in rows')
    rhpd = buildRowHiddenPairDict(canidates)
    printRowHiddenPairsDict(rhpd)

    for k,v in rhpd.items():
        rIdx     = rhpd[k]['row']
        cols     = rhpd[k]['cols']
        vals2Rmv = rhpd[k]['vals'] 

        for cIdx in cols:
            if canidates[rIdx][cIdx] != 0:
                for ii in range(1,10):
                    if ii in canidates[rIdx][cIdx] and ii not in vals2Rmv:
                        canidates[rIdx][cIdx].remove(ii)
                        print('    Removed {} from ({},{})'.format(ii, rIdx,cIdx))
                        numPruned += 1

    ####################################################################
    # Make a dict containing info on hidden pairs in each col.
    print('  Finding hidden pairs in cols')
    chpd = buildColHiddenPairDict(canidates)
    printColHiddenPairsDict(chpd)
    
    #pr.prettyPrint3DArray(canidates)
    for k,v in chpd.items():
        cIdx     = chpd[k]['col']
        rows     = chpd[k]['rows']
        vals2Rmv = chpd[k]['vals'] 
    
        for rIdx in rows:
            if canidates[rIdx][cIdx] != 0:
                for ii in range(1,10):
                    if ii in canidates[rIdx][cIdx] and ii not in vals2Rmv:
                        canidates[rIdx][cIdx].remove(ii)
                        print('    Removed {} from ({},{})'.format(ii, rIdx,cIdx))
                        numPruned += 1
    
    ####################################################################
    # Make a dict containing info on hidden pairs in each square.
    print('  Finding hidden pairs in squares')
    shpd = buildSqrHiddenPairDict(canidates)
    printSqrHiddenPairsDict(shpd)
    #pr.prettyPrint3DArray(canidates)
    
    for k,v in shpd.items():
        sIdx     = shpd[k][ 'sqr'  ]   
        idxs     = shpd[k][ 'idx'  ]
        vals2Rmv = shpd[k][ 'vals' ] 
        for idx in idxs:
    
            row              = ( idx // 3 ) + ( (sIdx // 3) * 3 )
            ofst1stCellInRow = ( row  * 9 ) + ( (sIdx %  3) * 3 )
            offsetInto_9x9   = ofst1stCellInRow + idx %  3
            col = offsetInto_9x9  % 9
            #print('sIdx, idx,   row, col = {:2d}, {:2d},   {:2d}, {:2d}'.format( sIdx, idx, row, col  ) )
    
            if canidates[row][col] != 0:
                for ii in range(1,10):
                    if ii in canidates[row][col] and ii not in vals2Rmv:
                        canidates[row][col].remove(ii)
                        print('    Removed {} from ({},{}) (sqr {})'.format(ii, row,col, sIdx))
                        numPruned += 1
    
    ###################################################################

    print('Pruning hidden pairs ** ( total pruned = {:2d} ) ********* End'.
        format(numPruned))
    #pr.prettyPrint3DArray(canidates)
    return numPruned, canidates
