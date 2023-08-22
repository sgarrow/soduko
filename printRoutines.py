def printCanidates(canidates):
    for rIdx,row in enumerate(canidates):     # for each row
        print('++------+------+------++------+------+------++------+------+------++')
        for ii in range(3):   # print 3 lines.
            thingsToPrint = list(range( ii*3+1, ii*3+4 )) # 1,2,3; 4,5,6; 7,8,9
            #print(thingsToPrint)
            print('|',end = '')
            for cIdx,cell in enumerate(row):
                for num in thingsToPrint:
                    if (num-1)%3 == 0: print('|',end = '')
                    if cell != 0 and num in cell:
                        print('{:2}'.format(num), end = '')
                    else:
                        print('  ',end = '')
                #if cIdx in [2,5]:  print('|',end = '') 
                if (cIdx+1)%3 == 0:  print('|',end = '') 
            print('|') # output 1st, 2nd or 3rd line of the row
        if (rIdx+1)%3 ==0:
            print('++------+------+------++------+------+------++------+------+------++')
    return 0
############################################################################
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

        print(' puzzle {}. {}. (numZeros = {})'.\
            format( key, 'FAIL' if puzzlesDict[key]['end0s'] else 'PASS',
                    puzzlesDict[key]['end0s'] ))

        if prnType == 'all':
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

        print( ' fillCellsVia_1_Canidate calls,replacements  = {:2d}, {:2d}.'.\
            format(puzzlesDict[key]['oC'], puzzlesDict[key]['oR']))

        print( ' fillCellsViaRowHistAnal calls,replacements  = {:2d}, {:2d}.'.\
            format(puzzlesDict[key]['rC'], puzzlesDict[key]['rR']))

        print( ' fillCellsViaColHistAnal calls,replacements  = {:2d}, {:2d}.'.\
            format(puzzlesDict[key]['cC'], puzzlesDict[key]['cR']))

        print( ' fillCellsViaSqrHistAnal calls,replacements  = {:2d}, {:2d}.'.\
            format(puzzlesDict[key]['sC'], puzzlesDict[key]['sR']))

        print(62*'*')                     

    return
#############################################################################

