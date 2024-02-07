#  C:\Users\bendr\AppData\Roaming\Python\Python311\Scripts\pylint.exe  .\soduko.py

import pprint        as pp
import printRoutines as pr
import mapping       as mp
import fillRoutines  as fr
import pruneRoutines as rr

NEWLINE = '\n'
STARS44 = 44*'*'
POUND62 = 62*'#'
#############################################################################

def updateCanidatesList(lclSolution,lclCanidates):
    print('\nUpdating Canidates list')
    cols = [ [ row[i] for row in lclSolution] for i in range(len(lclSolution[0]))]

    for rIdx,row in enumerate(lclSolution):
        for cIdx,elem in enumerate(row):
            col = cols[cIdx]

            if elem != 0:
                lclCanidates[rIdx][cIdx] = 0
                continue
            for num in [1,2,3,4,5,6,7,8,9]:

                inSquare = False
                rowsInSquare, colsInSquare = mp.findRowsColsInSquare(rIdx, cIdx)

                for ris in rowsInSquare:
                    for cis in colsInSquare:
                        if lclSolution[ris][cis] == num:
                            inSquare = True
                            break
                    if inSquare:
                        break

                #print('   inSquare={}'.format(inSquare))
                if( row.count(num) == 0 and col.count(num) == 0 and not inSquare):
                    #print('   Adding {} as canidate for {},{}'.format(ii,rIdx,cIdx))
                    if lclCanidates[rIdx][cIdx] != 0:
                        lclCanidates[rIdx][cIdx].append(num)
    totSum = 0
    for rIdx,row in enumerate(lclCanidates):
        for cIdx,elem in enumerate(row):
            if lclCanidates[rIdx][cIdx] != 0:
                totSum += sum(lclCanidates[rIdx][cIdx])
    print('totSum = ', totSum)
    return lclCanidates
#############################################################################

def updatePuzzlesDictCntrs(lclPuzzlesDict,k, lclfillDicOfFuncs):
    lclPuzzlesDict[k]['oC'] = lclfillDicOfFuncs['one']['calls'  ]
    lclPuzzlesDict[k]['oR'] = lclfillDicOfFuncs['one']['replace']
    lclPuzzlesDict[k]['rC'] = lclfillDicOfFuncs['row']['calls'  ]
    lclPuzzlesDict[k]['rR'] = lclfillDicOfFuncs['row']['replace']
    lclPuzzlesDict[k]['cC'] = lclfillDicOfFuncs['col']['calls'  ]
    lclPuzzlesDict[k]['cR'] = lclfillDicOfFuncs['col']['replace']
    lclPuzzlesDict[k]['sC'] = lclfillDicOfFuncs['sqr']['calls'  ]
    lclPuzzlesDict[k]['sR'] = lclfillDicOfFuncs['sqr']['replace']
    return lclPuzzlesDict
#############################################################################

def pruneNht(lclCanidates, clArgs):
    hiddenNakedLst = [ 'hidden', 'naked' ]
    houseLst       = [ 'row','col','sqr' ]
    tupSizeLst     = [4,3,2]
    #tupSizeLst     = [3,2]
    totNumPruned   = 0

    for hideNkd in hiddenNakedLst:
        for tupSize in tupSizeLst:
            for house in houseLst:
                #print('Pruning {:6} {}-tuples in {}s'.format(hn,N,h))
                numPruned, lclCanidates = \
                rr.pruneNakedAndHiddenTuples(lclCanidates, house, hideNkd, tupSize, clArgs)
                totNumPruned += numPruned

                if numPruned:
                    print(f'    Prunned {numPruned:2} RE: {hideNkd:6} {tupSize}-tuples in {house}s')

    #exit()
    return totNumPruned, lclCanidates
#############################################################################

def pruneXw(lclCanidates, clArgs):
    totNumPruned = 0
    houseLst = [ 'row','col' ]
    for house in houseLst:
        numPruned, lclCanidates = rr.pruneXwings(lclCanidates, house, clArgs)
        totNumPruned += numPruned

        if numPruned:
            print(f'    Prunned {numPruned:2} lclCanidates RE: X-Wings in {house}s')

    return totNumPruned, lclCanidates
#############################################################################

def pruneYw(lclCanidates, clArgs):
    totNumPruned = 0
    numPruned, lclCanidates = rr.pruneyWings(lclCanidates, clArgs)
    totNumPruned += numPruned

    if numPruned:
        print(f'    Prunned {numPruned:2} lclCanidates RE: Y-Wings.')

    return totNumPruned, lclCanidates
#############################################################################

def prunePp(lclCanidates, clArgs):
    totNumPruned = 0
    houseLst = [ 'row','col' ]
    #houseLst = [ 'row']
    for house in houseLst:
        numPruned, lclCanidates = rr.prunePointingPairs(lclCanidates, house, clArgs)
        totNumPruned += numPruned

        if numPruned:
            print(f'    Prunned {numPruned:2} lclCanidates RE: Pointing Pairs in rows')

    return totNumPruned, lclCanidates
#############################################################################

def pruneCanidates(clArgs, lclPruneDicOfFuncs, lclCanidates):
    #numPrunedPerPass
    print('\nPruning canidates list')

    prunedAtLeastOne   = True
    cumStr = ''
    while prunedAtLeastOne:                      # Loop over function group.

        prunedAtLeastOne   = False

        for k,v in lclPruneDicOfFuncs.items():   # Loop over each function.

            if v['func'] == pruneXw  and 'xwOff'  in clArgs: continue
            if v['func'] == pruneNht and 'nhtOff' in clArgs: continue
            if v['func'] == prunePp  and 'ppOff'  in clArgs: continue
            if v['func'] == pruneYw  and 'ywOff'  in clArgs: continue

            passNum            = 0
            numPrunnedThisPass = 0
            numPrunnedThisLoop = []

            while True:                          # Loop over one function.

                print('  {:9} pass {}'.format(k, passNum))
                numPrunnedThisPass, lclCanidates = v['func'](lclCanidates, clArgs)
                numPrunnedThisLoop.append(numPrunnedThisPass)
                if numPrunnedThisPass != 0:
                    cumStr += (f'  {k:9} prunned {numPrunnedThisPass}{NEWLINE}')
                passNum += 1

                if 'ss' in clArgs: input('Return to continue')

                if numPrunnedThisPass > 0:
                    prunedAtLeastOne = True
                else:
                    break

            v['numPrunned'].append(numPrunnedThisLoop)
            print('  Total Prunned {:9} {}'.format(k, sum(v['numPrunned'][-1])))
            print(31*'*')

        print(31*'*')

    print(cumStr)
    print(62*'*')

    return lclPruneDicOfFuncs, lclCanidates
#############################################################################

def fillSolution(lclSolution, lclCanidates, lclfillDicOfFuncs, clArgs ):
    totalNumFilled = 0

    print('\nFilling in solution cells')
    for k in lclfillDicOfFuncs:
        numFilled, lclSolution = lclfillDicOfFuncs[k]['func']( lclSolution, lclCanidates )
        totalNumFilled  += numFilled
        lclfillDicOfFuncs[k]['calls']   += 1
        lclfillDicOfFuncs[k]['replace'] += numFilled
        if 'ss' in clArgs: input('Return to continue')
    print(f'{NEWLINE}  Total filled {totalNumFilled:2d} {STARS44}')
    print(62*'*')

    return totalNumFilled, lclSolution, lclfillDicOfFuncs
#############################################################################

def initfillDicOfFuncsCntrs(lclfillDicOfFuncs):
    for k in lclfillDicOfFuncs:
        lclfillDicOfFuncs[k]['calls'  ] = 0
        lclfillDicOfFuncs[k]['replace'] = 0
    return lclfillDicOfFuncs
#############################################################################

if __name__ == '__main__':
    from puzzles import puzzlesDict

    fillDicOfFuncs = {
    'one': { 'func': fr.fillCellsViaOneCanidate, 'calls': 0, 'replace': 0 },
    'row': { 'func': fr.fillCellsViaRowHistAnal, 'calls': 0, 'replace': 0 },
    'col': { 'func': fr.fillCellsViaColHistAnal, 'calls': 0, 'replace': 0 },
    'sqr': { 'func': fr.fillCellsViaSqrHistAnal, 'calls': 0, 'replace': 0 }}

    pruneDicOfFuncs = {
    'prune_XW' : { 'func': pruneXw,  'numPrunned': []},
    'prune_NHT': { 'func': pruneNht, 'numPrunned': []},
    'prune_PP' : { 'func': prunePp,  'numPrunned': []},
    'prune_YW' : { 'func': pruneYw,  'numPrunned': []}}

    ###########################################################
    puzDicKeys = [ k for k in puzzlesDict.keys() ]
    print()
    for ii,k in enumerate(puzDicKeys):
        print('  {:2} - {}'.format( ii,k ))
    print( '   a - all')
    print( '   q - quit')
    puzIdxs = input('\n Choice -> ' ).split()

    if 'q' in puzIdxs:
        exit()

    if 'a' in puzIdxs:
        dsrdKeys = [ puzDicKeys[    x ] for x in range(len(puzDicKeys))]  
    else:
        dsrdKeys = [ puzDicKeys[int(x)] for x in puzIdxs] 
        print(puzIdxs, dsrdKeys)
    #input()
    ###########################################################
    with open('cfgFile.txt') as cfgFile:
        cmdLineArgs  = cfgFile.read().split()
    ###########################################################

    for key,val in puzzlesDict.items():

        if puzIdxs != 'a':
            if key not in dsrdKeys: 
                continue

        solution = [x[:] for x in val['puzzle'] ]
        val['start0s'] = sum(x.count(0) for x in solution)
        fillDicOfFuncs = initfillDicOfFuncsCntrs(fillDicOfFuncs)

        print(f'Processing puzzle {key}')
        while True:
            numZerosBeforeAllFill = sum(x.count(0) for x in solution)
            if sum(x.count(0) for x in solution)==0:
                break
            NUMBER_FILLED = 1
            while NUMBER_FILLED:

                if sum(x.count(0) for x in solution)==0:
                    break

                canidates = [[ [] for ii in range(9)] for jj in range(9)]
                canidates = updateCanidatesList(solution, canidates)

                pruneDicOfFuncs,canidates = \
                    pruneCanidates(cmdLineArgs, pruneDicOfFuncs, canidates)
                NUMBER_FILLED, solution, fillDicOfFuncs = \
                    fillSolution(solution, canidates, fillDicOfFuncs, cmdLineArgs)

            numZerosAfterAllFill = sum(x.count(0) for x in solution)
            if  numZerosAfterAllFill in (numZerosBeforeAllFill,0):
                break
            numZerosBeforeAllFill = numZerosAfterAllFill
        # end while loop for this puzzle
        val['end0s'] = numZerosAfterAllFill
        puzzlesDict = updatePuzzlesDictCntrs(puzzlesDict,key, fillDicOfFuncs)
        val['solution'] = solution
        print(f'{POUND62}')
    # end for loop on all puzzles

    pr.printResults(puzzlesDict, 'all', dsrdKeys)
    pr.printResults(puzzlesDict, 'summary', dsrdKeys)
