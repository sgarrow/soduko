import pprint        as pp
#############################################################################

def printRowNakedPairsLst(rowNakedPairsLst):
    if rowNakedPairsLst == [[],[],[],[],[],[],[],[],[]]:
        print( '  No row naked pairs found') 
        return
    for rIdx,currListOfDupPairs in enumerate(rowNakedPairsLst):
        if currListOfDupPairs != []:
            for idxOfCurrDupPair,currDupPairAndCoord in enumerate(currListOfDupPairs):
                print( '  Row {} contains naked pair {} at cols {}.'.\
                    format(rIdx,currDupPairAndCoord[0], currDupPairAndCoord[1]))
    return
#############################################################################

def printColNakedPairsLst(colNakedPairsLst):
    if colNakedPairsLst == [[],[],[],[],[],[],[],[],[]]:
        print( '  No col naked pairs found') 
        return
    for cIdx,currListOfDupPairs in enumerate(colNakedPairsLst):
        if currListOfDupPairs != []:
            for idxOfCurrDupPair,currDupPairAndCoord in enumerate(currListOfDupPairs):
                print( '  Col {} contains naked pair {} at rows {}.'.\
                    format(cIdx,currDupPairAndCoord[0], currDupPairAndCoord[1]))
    return
#############################################################################

def printSqrNakedPairsLst(sqrNakedPairsLst):
    if sqrNakedPairsLst == [[],[],[],[],[],[],[],[],[]]:
        print( '  No sqr naked pairs found') 
        return
    for sIdx,currListOfDupPairs in enumerate(sqrNakedPairsLst):
        if currListOfDupPairs != []:
            for currDupPair in currListOfDupPairs:
                print( '  Sqr {} contains naked pair {}.'.\
                    format(sIdx,currDupPair))
    return
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

def prettyPrint3DArray(array):
    for row in array:
        str1 = ' '.join(str(e).ljust(21) for e in row)
        print('  ',str1)
    print()
    return
#############################################################################

def printResults(puzzlesDict, prnType):
    print()
    for key in puzzlesDict:
        print()

        print(' puzzle {}. {}. (numZeros = {})'.\
            format( key, 'FAIL' if puzzlesDict[key]['end0s'] else 'PASS',
                    puzzlesDict[key]['end0s'] ))

        if prnType == 'all':
            print()
            for ii in range(len(puzzlesDict[key]['puzzle'])):
                print( puzzlesDict[key]['puzzle'  ][ii], '  ',  
                       puzzlesDict[key]['solution'][ii]  )

        print( '\n starting, ending zeros                      = {:2d}, {:2d}.'.\
            format(puzzlesDict[key]['start0s'], puzzlesDict[key]['end0s']))

        print( ' fillCellsVia_1_Canidate calls,replacements  = {:2d}, {:2d}.'.\
            format(puzzlesDict[key]['oC'], puzzlesDict[key]['oR']))

        print( ' fillCellsViaRowHistAnal calls,replacements  = {:2d}, {:2d}.'.\
            format(puzzlesDict[key]['rC'], puzzlesDict[key]['rR']))

        print( ' fillCellsViaColHistAnal calls,replacements  = {:2d}, {:2d}.'.\
            format(puzzlesDict[key]['cC'], puzzlesDict[key]['cR']))

        print( ' fillCellsViaSqrHistAnal calls,replacements  = {:2d}, {:2d}.'.\
            format(puzzlesDict[key]['sC'], puzzlesDict[key]['sR']))

        print('***********************************************************')

    return
#############################################################################

