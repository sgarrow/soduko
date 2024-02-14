def printCanidates(canidates):
    print('   c0  c1  c2   c3  c4  c5   c6  c7  c8  ')
    for rIdx,row in enumerate(canidates):     # for each row
        print('++---+---+---++---+---+---++---+---+---++')
        numPrintedThisRow = False
        for ii in range(3):   # print 3 lines.

            numPrintedThisLine = False
            lineToPrn = ''
            thingsToPrint = list(range( ii*3+1, ii*3+4 )) # 1,2,3; 4,5,6; 7,8,9
            #print(thingsToPrint)
            lineToPrn += '|'
            for cIdx,cell in enumerate(row):
                for num in thingsToPrint:
                    if (num-1)%3 == 0:
                        lineToPrn += '|'
                    if cell != 0 and num in cell:
                        lineToPrn += f'{num:1}'
                        numPrintedThisLine = True
                        numPrintedThisRow  = True
                    else:
                        lineToPrn += ' '
                if (cIdx+1)%3 == 0:
                    lineToPrn += '|'
            lineToPrn += f'| r{rIdx}'

            if numPrintedThisLine:
                print(lineToPrn)
            if not numPrintedThisRow and ii == 2:
                print(lineToPrn)

        if (rIdx+1)%3 ==0:
            print('++---+---+---++---+---+---++---+---+---++')
############################################################################
def prettyPrint3DArray(array):
    print()
    for row in array:
        str1 = ' '.join(str(e).ljust(21) for e in row)
        print('  ',str1)
    print()
#############################################################################

def printResults(puzzlesDict, prnType, dsrdKeys, lclArgs):
    print()

    cumSumStr = ''
    for key in puzzlesDict:

        if key not in dsrdKeys:
            continue

        sumStr = ' puzzle {:9} (numZeros = {:2}). {} (args = {}).\n'.\
                   format( key, puzzlesDict[key]['end0s'],
                   'FAIL' if puzzlesDict[key]['end0s'] else 'PASS',
                   puzzlesDict[key]['prunes'] )
        cumSumStr += sumStr

        if prnType == 'all':
            print(sumStr)

            print()
            for ii in range(len(puzzlesDict[key]['puzzle'])):
                print( '',puzzlesDict[key]['puzzle'  ][ii], '  ',
                       puzzlesDict[key]['solution'][ii]  )
            print()

            print( ' Starting: filled-in + not-filled-in = {:2d}+{:2d} = {:2d}.'.\
                format( 81-puzzlesDict[key]['start0s'],  puzzlesDict[key]['start0s'],
                        81-puzzlesDict[key]['start0s'] + puzzlesDict[key]['start0s'] ))

            print( ' Ending:   filled-in + not-filled-in = {:2d}+{:2d} = {:2d}.'.\
                format( 81-puzzlesDict[key]['end0s'],  puzzlesDict[key]['end0s'],
                        81-puzzlesDict[key]['end0s'] + puzzlesDict[key]['end0s'] ))

            print( ' fillViaOneCanidate calls,replacements  = {:2d}, {:2d}.'.\
                format(puzzlesDict[key]['oC'], puzzlesDict[key]['oR']))

            print( ' fillViaRowHistAnal calls,replacements  = {:2d}, {:2d}.'.\
                format(puzzlesDict[key]['rC'], puzzlesDict[key]['rR']))

            print( ' fillViaColHistAnal calls,replacements  = {:2d}, {:2d}.'.\
                format(puzzlesDict[key]['cC'], puzzlesDict[key]['cR']))

            print( ' fillViaSqrHistAnal calls,replacements  = {:2d}, {:2d}.'.\
                format(puzzlesDict[key]['sC'], puzzlesDict[key]['sR']))

            print(62*'*')
    if prnType == 'all':
        return sumStr
    else:
        return cumSumStr
#############################################################################
