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
        print('   Col {} has hidden pair {} in rows {}'.\
            format(shpd[k]['col'], shpd[k]['vals'], shpd[k]['rows']))
    return
#############################################################################

def buildRowHiddenPairDict(canidates):

    #pr.prettyPrint3DArray(canidates)
    binsHeightTwoThisRow = []
    binsHeightTwoAllRows = []
    for rIdx,row in enumerate(canidates):
        flatRow = fr.flatten(row)
        rowHist = fr.genHistogram(flatRow)
        binsHeightTwoThisRow = [ x[0] for x in rowHist if x[1] == 2 and x[0] != 0 ]
        binsHeightTwoAllRows.append(binsHeightTwoThisRow)
    #print('\nvalues that appear exactly twice on a given row')
    #pp.pprint(binsHeightTwoAllRows)

    lstOfDict = []
    for rIdx,binHeight2Row in enumerate(binsHeightTwoAllRows):
        myDict = {}
        for val in binHeight2Row:
            myDict[val] = [cIdx for cIdx, x in enumerate(canidates[rIdx]) if x != 0 and val in canidates[rIdx][cIdx]]
        lstOfDict.append(myDict)
    #print('\nvalueThatApearsExactlyTwice : theColsWhereTheyAppear (on a given row)')
    #pp.pprint(lstOfDict)

    itemNum = 0
    hiddenPairsDict = {}
    for rIdx,aDict in enumerate(lstOfDict):
        aDictValues = list(aDict.values()) # values are the cols
        #print(  'aDict.values()', aDict.values())
        for val in aDictValues:
            theCount = aDictValues.count(val)
            if theCount == 2:
                keysOfThisVal = [ k for k,v in aDict.items() if v == val ] # keys are the vals
                hiddenPairsDict[itemNum] = { 'row' : rIdx, 'cols' : val, 'vals' : keysOfThisVal }
                itemNum += 1
    #print('\nhiddenPairsDict')
    #pp.pprint(hiddenPairsDict)

    itemNum = 0
    hiddenPairsDict2 = {}
    for key,value in hiddenPairsDict.items():
        if value not in hiddenPairsDict2.values():
            hiddenPairsDict2[itemNum] = value
            itemNum += 1
    #print('\nhiddenPairsDict2 rows')
    #pp.pprint(hiddenPairsDict2)
    #exit()
    return(hiddenPairsDict2)
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

    pr.prettyPrint3DArray(canidates)
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

    print()
    print('\n canidatesAllSqr')
    pp.pprint(canidatesAllSqr)
    print()
    print('\nbinsHeightTwoAllSqrs: values that appear exactly twice in a given square')
    pp.pprint(binsHeightTwoAllSqrs)


    lstOfDict = []
    for sIdx,binHeight2Sqr in enumerate(binsHeightTwoAllSqrs):
        myDict = {}
        for val in binHeight2Sqr:
            myDict[val] = [idx for idx,x in enumerate(canidatesAllSqr[sIdx]) if x != 0 and val in canidatesAllSqr[sIdx][idx] ]
        lstOfDict.append(myDict)
    print('\nvalueThatApearsExactlyTwice : theIndexWhereTheyAppear (on a given square)')
    pp.pprint(lstOfDict)

    itemNum = 0
    hiddenPairsDict = {}
    for rIdx,aDict in enumerate(lstOfDict):
        aDictValues = list(aDict.values()) # values are the index in the square 1-9
        #print(  'aDict.values()', aDict.values())
        for val in aDictValues:
            theCount = aDictValues.count(val)
            if theCount == 2:
                keysOfThisVal = [ k for k,v in aDict.items() if v == val ] # keys are the vals
                hiddenPairsDict[itemNum] = { 'row' : rIdx, 'cols' : val, 'vals' : keysOfThisVal }
                itemNum += 1
    print('\nhiddenPairsDict')
    pp.pprint(hiddenPairsDict)

    itemNum = 0
    hiddenPairsDict2 = {}
    for key,value in hiddenPairsDict.items():
        if value not in hiddenPairsDict2.values():
            hiddenPairsDict2[itemNum] = value
            itemNum += 1
    print('\nhiddenPairsDict2 sqr')
    pp.pprint(hiddenPairsDict2)
    exit()

    #pr.prettyPrint3DArray(canidates)
    return
    #return(hiddenPairsDict2)
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
    print('  Finding hidden pairs in squares $$$$$$$$$$$$$$$$$$$')

    shpd = buildSqrHiddenPairDict(canidates)
    print('\nprintSqrHiddenPairsDict')
    printSqrHiddenPairsDict(chpd)
    print()
    exit()
    #pr.prettyPrint3DArray(canidates)
    #for k,v in chpd.items():
    #    cIdx     = chpd[k]['col']
    #    rows     = chpd[k]['rows']
    #    vals2Rmv = chpd[k]['vals'] 
    #
    #    for rIdx in rows:
    #        if canidates[rIdx][cIdx] != 0:
    #            for ii in range(1,10):
    #                if ii in canidates[rIdx][cIdx] and ii not in vals2Rmv:
    #                    canidates[rIdx][cIdx].remove(ii)
    #                    print('    Removed {} from ({},{})'.format(ii, rIdx,cIdx))
    #                    numPruned += 1

    print('Pruning hidden pairs ************************************* End')
    #pr.prettyPrint3DArray(canidates)

    return numPruned, canidates

    

