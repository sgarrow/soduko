import pprint        as pp
import fillRoutines  as fr
import printRoutines as pr

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
    nakedOrHiddenPairsDict = {}
    for rIdx,aDict in enumerate(lstOfDict):
        aDictValues = list(aDict.values()) # values are the cols
        #print(  'aDict.values()', aDict.values())
        for val in aDictValues:
            theCount = aDictValues.count(val)
            if theCount == 2:
                keysOfThisVal = [ k for k,v in aDict.items() if v == val ] # keys are the vals
                nakedOrHiddenPairsDict[itemNum] = { 'row' : rIdx, 'cols' : val, 'vals' : keysOfThisVal }
                itemNum += 1
    #print('\nnakedOrHiddenPairsDict')
    #pp.pprint(nakedOrHiddenPairsDict)

    itemNum = 0
    nakedOrHiddenPairsDict2 = {}
    for key,value in nakedOrHiddenPairsDict.items():
        if value not in nakedOrHiddenPairsDict2.values():
            nakedOrHiddenPairsDict2[itemNum] = value
            itemNum += 1
    #print('\nnakedOrHiddenPairsDict2')
    #pp.pprint(nakedOrHiddenPairsDict2)

    return(nakedOrHiddenPairsDict2)
#############################################################################

def pruneHiddenPairs(canidates):

    print('\nPruning hidden pairs')
    #pr.prettyPrint3DArray(canidates)
    numPruned = 0

    ####################################################################
    # Make a dict containing info on hidden pairs in each row.
    print('  Finding hidden pairs in rows')
    rhpd = buildRowHiddenPairDict(canidates)
    pr.printRowHiddenPairsDict(rhpd)

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
    print()

    return numPruned, canidates

    

