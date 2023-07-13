import pprint        as pp
import fillRoutines  as fr

def buildRowHiddenPairLst(canidates):

    binsHeightTwoThisRow = []
    binsHeightTwoAllRows = []
    for rIdx,row in enumerate(canidates):
        flatRow = fr.flatten(row)
        rowHist = fr.genHistogram(flatRow)
        binsHeightTwoThisRow = [ x[0] for x in rowHist if x[1] == 2 and x[0] != 0 ]
        binsHeightTwoAllRows.append(binsHeightTwoThisRow)
        #print(rowHist)
        #print(binsHeightTwoThisRow)
        #print()

    print()
    pp.pprint(binsHeightTwoAllRows)
    print()

    lstOfDict = []
    for rIdx,binHeight2Row in enumerate(binsHeightTwoAllRows):
        myDict = {}
        for val in binHeight2Row:
            myDict[val] = [cIdx for cIdx, x in enumerate(canidates[rIdx]) if x != 0 and val in canidates[rIdx][cIdx]]
        pp.pprint(myDict)
        lstOfDict.append(myDict)
    pp.pprint(myDict)
    return(lstOfDict)
    

