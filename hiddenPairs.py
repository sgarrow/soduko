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

def buildRowHiddenPairDict(canidates):

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
    #print('\nhiddenPairsDict2')
    #pp.pprint(hiddenPairsDict2)

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
                for ii in range(9):
                    if ii in canidates[rIdx][cIdx] and ii not in vals2Rmv:
                        canidates[rIdx][cIdx].remove(ii)
                        print('    Removed {} from ({},{})'.format(ii, rIdx,cIdx))
                        numPruned += 1
    print('Pruning hidden pairs ************************************* End')

    return numPruned, canidates

    

