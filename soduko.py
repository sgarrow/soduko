#  C:\Users\bendr\AppData\Roaming\Python\Python311\Scripts\pylint.exe  .\soduko.py

import pprint        as pp
import sys
import time
from itertools import combinations
import printRoutines as pr
import mapping       as mp
import fillRoutines  as fr
import pruneRoutines as rr
import ana           as an
import fillRoutines  as fr

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
    #print('totSum = ', totSum)
    return lclCanidates
#############################################################################

def pruneNht(lclCanidates, clArgs):

    hiddenNakedLst = [ 'hidden', 'naked' ]
    #hiddenNakedLst = [ 'hidden']

    houseLst       = [ 'row','col','sqr' ]
    #houseLst       = [ 'row' ]

    tupSizeLst     = [4,3,2]
    #tupSizeLst     = [3]

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
            print(f'    Prunned {numPruned:2} lclCanidates RE: Pointing Pairs in {house}')

    return totNumPruned, lclCanidates
#############################################################################

def pruneCanidates(clArgs, lclPruneDicOfFuncs, lclCanidates):
    print('\nPruning canidates list')

    prunedAtLeastOne   = True
    cumStr = ''
    while prunedAtLeastOne:                      # Loop over function group.

        prunedAtLeastOne   = False

        for theKey,v in lclPruneDicOfFuncs.items():   # Loop over each function.

            if v['func'] is pruneXw  and not 'xwOn' in clArgs: continue
            if v['func'] is pruneNht and not 'nhOn' in clArgs: continue
            if v['func'] is prunePp  and not 'ppOn' in clArgs: continue
            if v['func'] is pruneYw  and not 'ywOn' in clArgs: continue

            passNum            = 0
            numPrunnedThisPass = 0
            numPrunnedThisLoop = []

            while True:                          # Loop over one function.

                print('  {:9} pass {}'.format(theKey, passNum))
                numPrunnedThisPass, lclCanidates = v['func'](lclCanidates, clArgs)
                numPrunnedThisLoop.append(numPrunnedThisPass)
                if numPrunnedThisPass != 0:
                    cumStr += (f'  {theKey:9} prunned {numPrunnedThisPass}{NEWLINE}')
                passNum += 1

                if 'ss' in clArgs: input('Return to continue')

                if numPrunnedThisPass > 0:
                    prunedAtLeastOne = True
                else:
                    break

            v['numPrunned'].append(numPrunnedThisLoop)
            print('  Total Prunned {:9} {}'.format(theKey, sum(v['numPrunned'][-1])))
            print(31*'*')

        print(31*'*')

    print(cumStr)
    print(62*'*')

    return lclPruneDicOfFuncs, lclCanidates
#############################################################################

def fillSolution(lclSolution, lclCanidates, lclfillDicOfFuncs, clArgs ):
    totalNumFilled = 0

    print('\nFilling in solution cells')
    for theK in lclfillDicOfFuncs:
        numFilled, lclSolution = lclfillDicOfFuncs[theK]['func'](lclSolution,lclCanidates)
        totalNumFilled  += numFilled
        lclfillDicOfFuncs[theK]['calls']   += 1
        lclfillDicOfFuncs[theK]['replace'] += numFilled
    print(f'{NEWLINE}  Total filled {totalNumFilled:2d} {STARS44}')
    print(62*'*')
    if 'ss' in clArgs: input('Return to continue')

    return totalNumFilled, lclSolution, lclfillDicOfFuncs
#############################################################################

def initfillDicOfFuncsCntrs(lclfillDicOfFuncs):
    for theK in lclfillDicOfFuncs:
        lclfillDicOfFuncs[theK]['calls'  ] = 0
        lclfillDicOfFuncs[theK]['replace'] = 0
    return lclfillDicOfFuncs
#############################################################################

def solvePuzzle(aPuzzleDict, lclCmdLineArgs):

    fillDicOfFuncs = {
    'one': { 'func': fr.fillViaOneCanidate, 'calls': 0, 'replace': 0 },
    'row': { 'func': fr.fillViaRowHistAnal, 'calls': 0, 'replace': 0 },
    'col': { 'func': fr.fillViaColHistAnal, 'calls': 0, 'replace': 0 },
    'sqr': { 'func': fr.fillViaSqrHistAnal, 'calls': 0, 'replace': 0 }}

    pruneDicOfFuncs = {
    'prune_XW' : { 'func': pruneXw,  'numPrunned': []},
    'prune_NHT': { 'func': pruneNht, 'numPrunned': []},
    'prune_PP' : { 'func': prunePp,  'numPrunned': []},
    'prune_YW' : { 'func': pruneYw,  'numPrunned': []}}
    ###########################################################

    solution = [x[:] for x in aPuzzleDict['puzzle'] ]
    aPuzzleDict['start0s'] = sum(x.count(0) for x in solution)
    fillDicOfFuncs = initfillDicOfFuncsCntrs(fillDicOfFuncs)

    while True:
        numZerosBeforeAllFill = sum(x.count(0) for x in solution)
        if sum(x.count(0) for x in solution)==0:
            break
        numberFilled = 1
        while numberFilled:

            if sum(x.count(0) for x in solution)==0:
                break

            canidates = [[ [] for ii in range(9)] for jj in range(9)]
            canidates = updateCanidatesList(solution, canidates)

            pruneDicOfFuncs,canidates = \
                pruneCanidates(lclCmdLineArgs, pruneDicOfFuncs, canidates)
            numberFilled, solution, fillDicOfFuncs = \
                fillSolution(solution, canidates, fillDicOfFuncs, lclCmdLineArgs)

        numZerosAfterAllFill = sum(x.count(0) for x in solution)
        if  numZerosAfterAllFill in (numZerosBeforeAllFill,0):
            break
        numZerosBeforeAllFill = numZerosAfterAllFill
    # end while loop for this puzzle

    aPuzzleDict['end0s']    = numZerosAfterAllFill
    aPuzzleDict['solution'] = solution
    aPuzzleDict['prunes']   = lclCmdLineArgs
    aPuzzleDict['oC']       = fillDicOfFuncs['one']['calls'  ]
    aPuzzleDict['oR']       = fillDicOfFuncs['one']['replace']
    aPuzzleDict['rC']       = fillDicOfFuncs['row']['calls'  ]
    aPuzzleDict['rR']       = fillDicOfFuncs['row']['replace']
    aPuzzleDict['cC']       = fillDicOfFuncs['col']['calls'  ]
    aPuzzleDict['cR']       = fillDicOfFuncs['col']['replace']
    aPuzzleDict['sC']       = fillDicOfFuncs['sqr']['calls'  ]
    aPuzzleDict['sR']       = fillDicOfFuncs['sqr']['replace']

    print(f'{POUND62}')
    return aPuzzleDict
#############################################################################


def getGuesses(lclSolution):
    tryDict    = {}
    tryValsLst = []

    lclCanidates = [[ [] for ii in range(9)] for jj in range(9)]
    lclCanidates = updateCanidatesList(lclSolution, lclCanidates)
    pr.printCanidates(lclCanidates)

    lenCanR0C02 = [ 0 if lclCanidates[0][c] == 0 else len(lclCanidates[0][c]) for c in range(0,3) ]
    lenCanR1C35 = [ 0 if lclCanidates[0][c] == 0 else len(lclCanidates[0][c]) for c in range(3,6) ]
    lenCanR2C68 = [ 0 if lclCanidates[0][c] == 0 else len(lclCanidates[0][c]) for c in range(6,9) ]

    idxOfMaxR0C02 = lenCanR0C02.index(max(lenCanR0C02))
    idxOfMaxR1C35 = lenCanR1C35.index(max(lenCanR1C35))
    idxOfMaxR2C68 = lenCanR2C68.index(max(lenCanR2C68))
    
    tryDict = { 
        (0,0+idxOfMaxR0C02): lclCanidates[0][0+idxOfMaxR0C02],
        (1,3+idxOfMaxR1C35): lclCanidates[1][3+idxOfMaxR1C35],
        (2,6+idxOfMaxR2C68): lclCanidates[2][6+idxOfMaxR2C68]
    }
    pp.pprint(tryDict)

    for g1 in tryDict[(0,0+idxOfMaxR0C02)]:
        for g2 in tryDict[(1,3+idxOfMaxR1C35)]:
            for g3 in tryDict[(2,6+idxOfMaxR2C68)]:
                tryValsLst.append([g1,g2,g3])
    pp.pprint(tryValsLst)

    return tryDict, tryValsLst
#############################################################################



if __name__ == '__main__':
    from puzzles import puzzlesDict

    puzDicKeys = [ k for k in puzzlesDict.keys() ]
    print()
    for ii,k in enumerate(puzDicKeys):
        print('  {:2} - {}'.format( ii,k ))
    print( '   a - all')
    print( '   q - quit')
    puzIdxs = input('\n Choice -> ' ).split()

    if 'q' in puzIdxs:
        sys.exit()

    if 'a' in puzIdxs:
        dsrdKeys = [ puzDicKeys[    x ] for x in range(len(puzDicKeys))]
    else:
        dsrdKeys = [ puzDicKeys[int(x)] for x in puzIdxs]

    #print(dsrdKeys)
    #exit()
    ###########################################################

    with open('cfgFile.txt', encoding='utf-8') as cfgFile:
        rawCmdLineArgs  = cfgFile.read().split()
    cmdLineArgs = [x for x in rawCmdLineArgs if not x.startswith('#')]
    ###########################################################

    pruneSet0 = set(combinations(cmdLineArgs, 0))
    pruneSet1 = set(combinations(cmdLineArgs, 1))
    pruneSet2 = set(combinations(cmdLineArgs, 2))
    pruneSet3 = set(combinations(cmdLineArgs, 3))
    pruneSet4 = set(combinations(cmdLineArgs, 4))
    allSets = set.union(pruneSet0, pruneSet1, pruneSet2, pruneSet3, pruneSet4)

    characterize = True
    #characterize = False

    guessDict = {}
    tryLst    = []
    cumAllStr = ''
    cumSumStr = ''

    for pNme in dsrdKeys:
        pDat = puzzlesDict[pNme]

        if characterize:

            for args in allSets:

                puzzlesDict[pNme] = solvePuzzle(pDat, args)
                aStr, sStr = pr.printResults(pNme, pDat)
                cumAllStr += aStr
                cumSumStr += sStr

        else:

            puzzlesDict[pNme] = solvePuzzle(pDat, cmdLineArgs)
            aStr, sStr = pr.printResults(pNme, pDat)
            cumAllStr += aStr
            cumSumStr += sStr

    print(cumAllStr)
    print(cumSumStr)

    if characterize:
        with open('pData.txt', 'w', encoding='utf-8') as pFile:
            pFile.write(cumSumStr)
        an.analyze()


