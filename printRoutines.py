def printCanidates(canidates,alreadyPrn = False):

    if alreadyPrn:
        return

    print('     c0  c1  c2   c3  c4  c5   c6  c7  c8  ')
    for rIdx,row in enumerate(canidates):     # for each row
        print('  ++---+---+---++---+---+---++---+---+---++')
        numPrintedThisRow = False
        for ii in range(3):   # print 3 lines.

            numPrintedThisLine = False
            lineToPrn = '  '
            thingsToPrint = list(range(ii*3+1, ii*3+4)) # 1,2,3; 4,5,6; 7,8,9
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
            print('  ++---+---+---++---+---+---++---+---+---++')
############################################################################
def prettyPrint3DArray(array):
    print()
    for row in array:
        str1 = ' '.join(str(e).ljust(21) for e in row)
        print('  ',str1)
    print()
#############################################################################

def prYWingDict(v):
    print('    cord   = {}'.format(v[ 'cord'   ]))
    print('    sqrs   = {}'.format(v[ 'sqrs'   ]))
    print('    vals   = {}'.format(v[ 'vals'   ]))
    print()

    print('    pIdx   = {}'.format(v[ 'pIdx'   ]))
    print('    Z      = {}'.format(v[ 'Z'      ]))
    print('    rmvIdx = {}'.format(v[ 'rmvIdx' ]))

    #print('    rSee   = {}'.format(v['rSee'][0]))
    #print('             {}'.format(v['rSee'][1]))
    #print('             {}'.format(v['rSee'][2]))

    #print('    cSee   = {}'.format(v['cSee'][0]))
    #print('             {}'.format(v['cSee'][1]))
    #print('             {}'.format(v['cSee'][2]))

    #print('    sSee   = {}'.format(v['sSee'][0]))
    #print('             {}'.format(v['sSee'][1]))
    #print('             {}'.format(v['sSee'][2]))

    #print('    aSee   = {}'.format(v['allSeeSet'][0]))
    #print('             {}'.format(v['allSeeSet'][1]))
    #print('             {}'.format(v['allSeeSet'][2]))
    print()
    return 0
#############################################################################
                                     #
def printResults(pNme, apDict):

    sumStr = ''
    allStr = ''

    pf     = 'FAIL' if not apDict['passed'] else 'PASS'
    sumStr += ' {:9} {} {}\n'.format( pNme, pf, apDict['prunes'] )

    allStr = '\n' + sumStr[:] + '\n'
    for ii in range(len(apDict['puzzle'])):
        allStr += ' {}   {}\n'.\
            format(apDict['puzzle'][ii], apDict['solution'][ii])

    allStr += '\n'

    allStr += ' Start: filled-in + not-filled-in = {:2d}+{:2d} = {:2d}.\n'.\
              format( 81-apDict['start0s'],  apDict['start0s'],
                      81-apDict['start0s'] + apDict['start0s'] )

    allStr += ' End:   filled-in + not-filled-in = {:2d}+{:2d} = {:2d}.\n\n'.\
              format( 81-apDict['end0s'],    apDict['end0s'],
                      81-apDict['end0s'] +   apDict['end0s']   )

    allStr += ' fillOneCan  calls,fills = {:2d}, {:2d}.\n'.\
        format(apDict['oC'], apDict['oR'])

    allStr += ' fillRowHist calls,fills = {:2d}, {:2d}.\n'.\
        format(apDict['rC'], apDict['rR'])

    allStr += ' fillColHist calls,fills = {:2d}, {:2d}.\n'.\
        format(apDict['cC'], apDict['cR'])

    allStr += ' fillSqrHist calls,fills = {:2d}, {:2d}.\n'.\
        format(apDict['sC'], apDict['sR'])

    allStr += 62*'*' + '\n'

    return allStr, sumStr
#############################################################################
