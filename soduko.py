#  C:\Users\bendr\AppData\Roaming\Python\Python311\Scripts\pylint.exe  .\soduko.py

import pprint        as pp
import sys
import time
from itertools import combinations
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
    #print('totSum = ', totSum)
    return lclCanidates
#############################################################################

def updatePuzzlesDictCntrs(lclPuzzlesDict,lclKey, lclfillDicOfFuncs):
    lclPuzzlesDict[lclKey]['oC'] = lclfillDicOfFuncs['one']['calls'  ]
    lclPuzzlesDict[lclKey]['oR'] = lclfillDicOfFuncs['one']['replace']
    lclPuzzlesDict[lclKey]['rC'] = lclfillDicOfFuncs['row']['calls'  ]
    lclPuzzlesDict[lclKey]['rR'] = lclfillDicOfFuncs['row']['replace']
    lclPuzzlesDict[lclKey]['cC'] = lclfillDicOfFuncs['col']['calls'  ]
    lclPuzzlesDict[lclKey]['cR'] = lclfillDicOfFuncs['col']['replace']
    lclPuzzlesDict[lclKey]['sC'] = lclfillDicOfFuncs['sqr']['calls'  ]
    lclPuzzlesDict[lclKey]['sR'] = lclfillDicOfFuncs['sqr']['replace']
    return lclPuzzlesDict
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
            print(f'    Prunned {numPruned:2} lclCanidates RE: Pointing Pairs in rows')

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
        if 'ss' in clArgs: input('Return to continue')
    print(f'{NEWLINE}  Total filled {totalNumFilled:2d} {STARS44}')
    print(62*'*')

    return totalNumFilled, lclSolution, lclfillDicOfFuncs
#############################################################################

def initfillDicOfFuncsCntrs(lclfillDicOfFuncs):
    for theK in lclfillDicOfFuncs:
        lclfillDicOfFuncs[theK]['calls'  ] = 0
        lclfillDicOfFuncs[theK]['replace'] = 0
    return lclfillDicOfFuncs
#############################################################################

def solvePuzzles(lclPuzzlesDict, lclPuzIdxs, lclCmdLineArgs):

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

    if 'q' in lclPuzIdxs:
        sys.exit()
    if 'a' in lclPuzIdxs:
        lclDsrdKeys = [ puzDicKeys[    x ] for x in range(len(puzDicKeys))]
    else:
        lclDsrdKeys = [ puzDicKeys[int(x)] for x in puzIdxs]
    #print(lclDsrdKeys)
    #input()
    ###########################################################

    for key,val in lclPuzzlesDict.items():
        time.sleep(0.01)
        if puzIdxs != 'a':
            if key not in lclDsrdKeys:
                continue

        solution = [x[:] for x in val['puzzle'] ]
        val['start0s'] = sum(x.count(0) for x in solution)
        fillDicOfFuncs = initfillDicOfFuncsCntrs(fillDicOfFuncs)

        print(f'Processing puzzle {key}')
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
        val['end0s'] = numZerosAfterAllFill
        lclPuzzlesDict = updatePuzzlesDictCntrs(lclPuzzlesDict, key, fillDicOfFuncs)
        val['solution'] = solution
        val['prunes'] = lclCmdLineArgs
        print(f'{POUND62}')
    # end for loop on all puzzles
    return lclDsrdKeys, lclPuzzlesDict
#############################################################################

if __name__ == '__main__':
    from puzzles import puzzlesDict

    print()
    print('  puzEsy_38 can PASS w/ :[\'0\']')
    print('  puzMed_32 can PASS w/ :[\'0\']')
    print('  puzHrd_29 can PASS w/ :[\'0\']')
    print('  puzExp_23 can PASS w/ :[\'0\']')
    print('  puzEvl_23 can PASS w/ :[\'0\']')
    print('  puzEv2_23 can PASS w/ :[\'0\']')
    print('  puzEv3_23 can PASS w/ :[\'nhOn\']')
    print('  puzXW_46  can PASS w/ :[\'xwOn\']')
    print('  puzYW_29  can PASS w/ :[\'nhOn_ywOn\', \'ppOn_ywOn\']')
    print('  puzYW_26  can PASS w/ :[\'ywOn\']')
    print('  puzUsr    can PASS w/ :[\'ppOn_ywOn\']')
    print('  puzMax_21 always FAILS')
    print()

    puzDicKeys = [ k for k in puzzlesDict.keys() ]
    print()
    for ii,k in enumerate(puzDicKeys):
        print('  {:2} - {}'.format( ii,k ))
    print( '   a - all')
    print( '   q - quit')
    puzIdxs = input('\n Choice -> ' ).split()

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
    pp.pprint(allSets)
    #sys.exit()

    characterize = True
    characterize = False

    cumSumStr = ''
    if characterize:
        for args in allSets:
            dsrdKeys, puzzlesDict = solvePuzzles(puzzlesDict, puzIdxs, args)
            cumSumStr += pr.printResults(puzzlesDict, 'summary', dsrdKeys, args)
        print(cumSumStr)
    else:
        dsrdKeys, puzzlesDict = solvePuzzles(puzzlesDict, puzIdxs, cmdLineArgs)
        pr.printResults(puzzlesDict, 'all'    , dsrdKeys, cmdLineArgs)
        cumSumStr += pr.printResults(puzzlesDict, 'summary', dsrdKeys, cmdLineArgs)
        print(cumSumStr)
        #pr.printCanidates(canidates)

