def prettyPrint3DArray(array):
    print()
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

        print( ' starting, ending non-zeros                  = {:2d}, {:2d}.'.\
            format(81-puzzlesDict[key]['start0s'], 81-puzzlesDict[key]['end0s']))

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

