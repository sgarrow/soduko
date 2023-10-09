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

def pruneNht(lclCanidates):
    hiddenNakedLst = [ 'hidden', 'naked' ]
    houseLst       = [ 'row','col','sqr' ]
    tupSizeLst     = [4,3,2]
    totNumPruned   = 0

    for hideNkd in hiddenNakedLst:
        for tupSize in tupSizeLst:
            for house in houseLst:
                #print('Pruning {:6} {}-tuples in {}s'.format(hn,N,h))
                numPruned, lclCanidates = \
                rr.pruneNakedAndHiddenTuples(lclCanidates, house, hideNkd, tupSize)
                totNumPruned += numPruned

                if numPruned:
                    print(f'    Prunned {numPruned:2} RE: {hideNkd:6} {tupSize}-tuples in {house}s')

    return totNumPruned, lclCanidates
#############################################################################

def pruneXw(lclCanidates):
    totNumPruned = 0
    houseLst = [ 'row','col' ]
    for house in houseLst:
        numPruned, lclCanidates = rr.pruneXwings(lclCanidates, house)
        totNumPruned += numPruned

        if numPruned:
            print(f'    Prunned {numPruned:2} lclCanidates RE: X-Wings in {house}s')

    return totNumPruned, lclCanidates
#############################################################################

def prunePp(lclCanidates):
    totNumPruned = 0
    numPruned, lclCanidates = rr.prunePointingPairs(lclCanidates)
    totNumPruned += numPruned

    if numPruned:
        print(f'    Prunned {numPruned:2} lclCanidates RE: Pointing Pairs in rows')

    return totNumPruned, lclCanidates
#############################################################################

def pruneCanidates(lclCanidates):

    print('\nPruning canidates list')

    pDict = {
    'prune_XW' : { 'func': pruneXw,   'passNum': 0, 'totNumPruned': 0},
    'prune_NHT': { 'func': pruneNht,  'passNum': 0, 'totNumPruned': 0},
    'prune_PP' : { 'func': prunePp,   'passNum': 0, 'totNumPruned': 0}}

    prunedAtLeastOne = True
    while prunedAtLeastOne:
        prunedAtLeastOne = False
        for k,v in pDict.items():
            numPruned = 1
            v['passNum'] = 0
            while numPruned:
                print('  {:9} pass {}'.format(k, v['passNum']))
                numPruned, lclCanidates = v['func'](lclCanidates)
                v['totNumPruned'] += numPruned
                print(f'  {k:9} prunned {numPruned}{NEWLINE}')
                v['passNum'] += 1
                if numPruned > 0:
                    prunedAtLeastOne = True

            print(31*'*')
        print(31*'*')

    totTotNumPruned = 0
    for k,v in pDict.items():
        print('  Total Prunned {:9} {:2} {}'.format(k, v['totNumPruned'], STARS33))
        totTotNumPruned += v['totNumPruned']
    print(62*'*')
    return totTotNumPruned, lclCanidates
#############################################################################

def fillSolution(lclSolution, lclCanidates, lclDicOfFuncs ):
    totalNumFilled = 0

    print('\nFilling in solution cells')
    for k in lclDicOfFuncs:
        numFilled, lclSolution = lclDicOfFuncs[k]['func']( lclSolution, lclCanidates )
        totalNumFilled  += numFilled
        lclDicOfFuncs[k]['calls']   += 1
        lclDicOfFuncs[k]['replace'] += numFilled
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

    dicOfFuncs = {
        'one': { 'func': fr.fillCellsViaOneCanidate, 'calls': 0, 'replace': 0 },
        'row': { 'func': fr.fillCellsViaRowHistAnal, 'calls': 0, 'replace': 0 },
        'col': { 'func': fr.fillCellsViaColHistAnal, 'calls': 0, 'replace': 0 },
        'sqr': { 'func': fr.fillCellsViaSqrHistAnal, 'calls': 0, 'replace': 0 }}

    print(puzzlesDict['puzzleEsy']['puzzle'])
    for key,val in puzzlesDict.items():
        print(f'Processing puzzle {key}')
        solution = [x[:] for x in val['puzzle'] ]
        val['start0s'] = sum(x.count(0) for x in solution)
        dicOfFuncs = initDicOfFuncsCntrs(dicOfFuncs)
        while True:
            numZerosBeforeAllFill = sum(x.count(0) for x in solution)
            if sum(x.count(0) for x in solution)==0:
                break
            NUMBER_FILLED = 1
            while NUMBER_FILLED:

                if sum(x.count(0) for x in solution)==0:
                    break

                canidates = [[ [] for ii in range(9)] for jj in range(9)]
                canidates = updateCanidatesList(solution, canidates )

                numberPruned, canidates = pruneCanidates(canidates)
                NUMBER_FILLED, solution, dicOfFuncs = fillSolution(solution, canidates, dicOfFuncs )

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
