''' A suduko puzzle is a partailly filled 2D array of 9 rows and 9 cols.
The puzzle can also be thought of a 9 3x3 sub-grids called squares.
So, threre are 9 rows, 9 colums and 9 squares. Like this:

    col0 col1 col2    col3 col4 col5   col6 col7 col8
  ++----+----+----+  +----+----+----+  +----+----+----++
  ||    |    |    |  |    |    |    |  |    |    |    || row0
  ++----+----+----+  +----+----+----+  +----+----+----++
  ||   square 0   |  |   square 1   |  |    |    |    || row1
  ++----+----+----+  +----+----+----+  +----+----+----++
  ||    |    |    |  |    |    |    |  |    |    |    || row2
  ++----+----+----+  +----+----+----+  +----+----+----++

  ++----+----+----+  +----+----+----+  +----+----+----++
  ||    |    |    |  |    |    |    |  |    |    |    || row3
  ++----+----+----+  +----+----+----+  +----+----+----++
  ||    |    |    |  |    |    |    |  |    |    |    || row4
  ++----+----+----+  +----+----+----+  +----+----+----++
  ||    |    |    |  |    |    |    |  |    |    |    || row5
  ++----+----+----+  +----+----+----+  +----+----+----++

  ++----+----+----+  +----+----+----+  +----+----+----++
  ||    |    |    |  |    |    |    |  |    |    |    || row6
  ++----+----+----+  +----+----+----+  +----+----+----++
  ||    |    |    |  |    |    |    |  |   square 8   || row7
  ++----+----+----+  +----+----+----+  +----+----+----++
  ||    |    |    |  |    |    |    |  |    |    |    || row8
  ++----+----+----+  +----+----+----+  +----+----+----++

Each of the 81 "cells" lives in 3 "houses", a row, a col and a square.
A solved puzzle has a number 1-9 in each of the 81 cells such that each 
number appears only once in each house.
'''
#  C:\Users\bendr\AppData\Roaming\Python\Python311\Scripts\pylint.exe  .\soduko.py

import pprint        as pp
import printRoutines as pr
import mapping       as mp
import fillRoutines  as fr
import pruneRoutines as rr

NEWLINE = '\n'
STARS33 = 33*'*'
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

def updatePuzzlesDictCntrs(lclPuzzlesDict,k, lclDicOfFuncs):
    lclPuzzlesDict[k]['oC'] = lclDicOfFuncs['one']['calls'  ]
    lclPuzzlesDict[k]['oR'] = lclDicOfFuncs['one']['replace']
    lclPuzzlesDict[k]['rC'] = lclDicOfFuncs['row']['calls'  ]
    lclPuzzlesDict[k]['rR'] = lclDicOfFuncs['row']['replace']
    lclPuzzlesDict[k]['cC'] = lclDicOfFuncs['col']['calls'  ]
    lclPuzzlesDict[k]['cR'] = lclDicOfFuncs['col']['replace']
    lclPuzzlesDict[k]['sC'] = lclDicOfFuncs['sqr']['calls'  ]
    lclPuzzlesDict[k]['sR'] = lclDicOfFuncs['sqr']['replace']
    return lclPuzzlesDict
#############################################################################

def pruneNht(lclCanidates, clArgs):
    hiddenNakedLst = [ 'hidden', 'naked' ]
    houseLst       = [ 'row','col','sqr' ]
    tupSizeLst     = [4,3,2]
    #tupSizeLst     = [2]
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

def pruneCanidates(lclCanidates, clArgs):

    print('\nPruning canidates list')
    #pr.prettyPrint3DArray(lclCanidates)

    pDict = {
    'prune_XW' : { 'func': pruneXw,   'passNum': 0, 'totNumPruned': 0},
    'prune_NHT': { 'func': pruneNht,  'passNum': 0, 'totNumPruned': 0},
    'prune_PP' : { 'func': prunePp,   'passNum': 0, 'totNumPruned': 0}}

    prunedAtLeastOne = True
    while prunedAtLeastOne:
        prunedAtLeastOne = False
        for k,v in pDict.items():

            if v['func'] == pruneXw  and 'xwOff'  in clArgs: continue
            if v['func'] == pruneNht and 'nhtOff' in clArgs: continue
            if v['func'] == prunePp  and 'ppOff'  in clArgs: continue

            numPruned = 1
            v['passNum'] = 0
            while numPruned:
                print('  {:9} pass {}'.format(k, v['passNum']))
                numPruned, lclCanidates = v['func'](lclCanidates, clArgs)
                v['totNumPruned'] += numPruned
                print(f'  {k:9} prunned {numPruned}{NEWLINE}')
                v['passNum'] += 1
                if numPruned > 0:
                    prunedAtLeastOne = True
                if 'ss' in clArgs: input('Return to continue')

            print(31*'*')
        print(31*'*')

    lclCanidates = rr.yWing(lclCanidates)
    totTotNumPruned = 0
    for k,v in pDict.items():
        print('  Total Prunned {:9} {:2} {}'.format(k, v['totNumPruned'], STARS33))
        totTotNumPruned += v['totNumPruned']
    print(62*'*')

    #pr.prettyPrint3DArray(lclCanidates)
    #input()
    return totTotNumPruned, lclCanidates
#############################################################################

def fillSolution(lclSolution, lclCanidates, lclDicOfFuncs, clArgs ):
    totalNumFilled = 0

    print('\nFilling in solution cells')
    for k in lclDicOfFuncs:
        numFilled, lclSolution = lclDicOfFuncs[k]['func']( lclSolution, lclCanidates )
        totalNumFilled  += numFilled
        lclDicOfFuncs[k]['calls']   += 1
        lclDicOfFuncs[k]['replace'] += numFilled
        if 'ss' in clArgs: input('Return to continue')
    print(f'{NEWLINE}  Total filled {totalNumFilled:2d} {STARS44}')
    print(62*'*')

    return totalNumFilled, lclSolution, lclDicOfFuncs
#############################################################################

def initDicOfFuncsCntrs(lclDicOfFuncs):
    for k in lclDicOfFuncs:
        lclDicOfFuncs[k]['calls'  ] = 0
        lclDicOfFuncs[k]['replace'] = 0
    return lclDicOfFuncs
#############################################################################

if __name__ == '__main__':
    from puzzles import puzzlesDict
    #rr.yWing(0)
    #exit()
    dicOfFuncs = {
        'one': { 'func': fr.fillCellsViaOneCanidate, 'calls': 0, 'replace': 0 },
        'row': { 'func': fr.fillCellsViaRowHistAnal, 'calls': 0, 'replace': 0 },
        'col': { 'func': fr.fillCellsViaColHistAnal, 'calls': 0, 'replace': 0 },
        'sqr': { 'func': fr.fillCellsViaSqrHistAnal, 'calls': 0, 'replace': 0 }}

    try:
        with open('cfgFile.txt') as cfgFile:
            cmdLineArgs  = cfgFile.read().split()
    except:
        cmdLineArgs = input(' Args-> ').split()

    for key,val in puzzlesDict.items():
        solution = [x[:] for x in val['puzzle'] ]
        val['start0s'] = sum(x.count(0) for x in solution)
        dicOfFuncs = initDicOfFuncsCntrs(dicOfFuncs)

        print(f'Processing puzzle {key}')
        #input()
        while True:
            numZerosBeforeAllFill = sum(x.count(0) for x in solution)
            if sum(x.count(0) for x in solution)==0:
                break
            NUMBER_FILLED = 1
            while NUMBER_FILLED:

                if sum(x.count(0) for x in solution)==0:
                    break

                canidates = [[ [] for ii in range(9)] for jj in range(9)]
                #pp.pprint(solution)
                #pr.prettyPrint3DArray(canidates)
                canidates = updateCanidatesList(solution, canidates )
                #pr.prettyPrint3DArray(canidates)
                #input()
                # TODO: remove those things already pruned

                numberPruned, canidates = pruneCanidates(canidates,cmdLineArgs)
                # update those pruned
                NUMBER_FILLED, solution, dicOfFuncs = fillSolution(solution, canidates, dicOfFuncs,cmdLineArgs)

            numZerosAfterAllFill = sum(x.count(0) for x in solution)
            if  numZerosAfterAllFill in (numZerosBeforeAllFill,0):
                break
            numZerosBeforeAllFill = numZerosAfterAllFill
        # end while loop for this puzzle
        val['end0s'] = numZerosAfterAllFill
        puzzlesDict = updatePuzzlesDictCntrs(puzzlesDict,key, dicOfFuncs)
        val['solution'] = solution
        print(f'{POUND62}')
    # end for loop on all puzzles

    pr.printResults(puzzlesDict, 'all')
    pr.printResults(puzzlesDict, 'summary')
    #pr.prettyPrint3DArray(canidates)
    #
    #for row in canidates:
    #    flatRow = fr.flatten(row)
    #    histRow = fr.genHistogram(flatRow)
    #    pp.pprint(histRow)





