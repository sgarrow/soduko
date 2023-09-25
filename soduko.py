# New comment for git2.
'''DocStr'''
import printRoutines as pr
import initRoutines  as ir
import fillRoutines  as fr
import pruneRoutines as rr
newline = '\n'
stars39 = 39*'*'
stars44 = 44*'*'
pound62 = 62*'#'
#############################################################################

def findRowsColsInSquare(rIdx, cIdx):
    '''DocStr'''
    if rIdx % 3 == 0:
        rOffsets = [ 1, 2]
    if rIdx % 3 == 1:
        rOffsets = [-1, 1]
    if rIdx % 3 == 2:
        rOffsets = [-1,-2]
    if cIdx % 3 == 0:
        cOffsets = [ 1, 2]
    if cIdx % 3 == 1:
        cOffsets = [-1, 1]
    if cIdx % 3 == 2:
        cOffsets = [-1,-2]
    rowsInSquare = [ rIdx+rOffsets[0], rIdx+rOffsets[1] ]
    colsInSquare = [ cIdx+cOffsets[0], cIdx+cOffsets[1] ]
    return rowsInSquare, colsInSquare
#############################################################################

def updateCanidatesList(lclSolution,lclCanidates):
    '''DocStr'''
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
                rowsInSquare, colsInSquare = findRowsColsInSquare(rIdx, cIdx)

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
    '''DocStr'''
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
    '''DocStr'''
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
    '''DocStr'''
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
    '''DocStr'''
    totNumPruned = 0
    numPruned, lclCanidates = rr.prunePointingPairs(lclCanidates)
    totNumPruned += numPruned

    if numPruned:
        print(f'    Prunned {numPruned:2} lclCanidates RE: Pointing Pairs in rows')

    return totNumPruned, lclCanidates
#############################################################################

def pruneCanidates(lclCanidates):
    '''DocStr'''

    print('\nPruning  lclCanidates list')
    totNumPrunedXw  = 0
    totNumPrunedNht = 0
    totNumPrunedPp  = 0
    passNumXw       = 0
    passNumNht      = 0
    passNumPp       = 0

    prunedAtLeastOne = True
    while prunedAtLeastOne:
        prunedAtLeastOne = False
        numPruned = 1
        while numPruned:
            print(f'  prune_XW  pass {passNumXw}')
            numPruned, lclCanidates = pruneXw(lclCanidates)
            totNumPrunedXw += numPruned
            print(f'  prune_XW  prunned {numPruned}{newline}')
            passNumXw += 1
            if numPruned > 0:
                prunedAtLeastOne = True

        numPruned = 1
        while numPruned:
            print(f'  prune_NHT pass {passNumNht}')
            numPruned, lclCanidates = pruneNht(lclCanidates)
            totNumPrunedNht += numPruned
            print(f'  prune_NHT  prunned {numPruned}{newline}')
            passNumNht += 1
            if numPruned > 0:
                prunedAtLeastOne = True

        numPruned = 1
        while numPruned:
            print(f'  prune_PP  pass {passNumPp}')
            numPruned, lclCanidates = prunePp(lclCanidates)
            totNumPrunedPp += numPruned
            print(f'  prune_PP  prunned {numPruned}{newline}')
            passNumPp += 1
            if numPruned > 0:
                prunedAtLeastOne = True
        print(31*'*')

    print(f'  Total Prunned NHT {totNumPrunedNht:2} {stars39}')
    print(f'  Total Prunned XW  {totNumPrunedXw :2} {stars39}')
    print(f'  Total Prunned PP  {totNumPrunedPp :2} {stars39}')
    print(62*'*')
    return totNumPrunedXw + totNumPrunedNht + totNumPrunedPp, lclCanidates
#############################################################################

def fillSolution(lclSolution, lclCanidates, lclDicOfFuncs ):
    '''DocStr'''
    totalNumFilled = 0

    print('\nFilling in solution cells')
    for k in dicOfFuncs:
        numFilled, lclSolution = lclDicOfFuncs[k]['func']( lclSolution, lclCanidates )
        totalNumFilled  += numFilled
        dicOfFuncs[k]['calls']   += 1
        dicOfFuncs[k]['replace'] += numFilled
    print(f'{newline}  Total filled {totalNumFilled:2d} {stars44}')
    print(62*'*')

    return totalNumFilled, lclSolution, lclDicOfFuncs
#############################################################################

if __name__ == '__main__':
    from puzzles import puzzlesDict

    dicOfFuncs = {
        'one': { 'func': fr.fillCellsViaOneCanidate, 'calls': 0, 'replace': 0 },
        'row': { 'func': fr.fillCellsViaRowHistAnal, 'calls': 0, 'replace': 0 },
        'col': { 'func': fr.fillCellsViaColHistAnal, 'calls': 0, 'replace': 0 },
        'sqr': { 'func': fr.fillCellsViaSqrHistAnal, 'calls': 0, 'replace': 0 }}

    for key,val in puzzlesDict.items():
        print(f'Processing puzzle {key}')
        solution = [x[:] for x in val['puzzle'] ]
        val['start0s'] = sum(x.count(0) for x in solution)
        dicOfFuncs = ir.initDicOfFuncsCntrs(dicOfFuncs)
        while True:
            numZerosBeforeAllFill = sum(x.count(0) for x in solution)
            if sum(x.count(0) for x in solution)==0:
                break
            numberFilled = 1
            while numberFilled:

                if sum(x.count(0) for x in solution)==0:
                    break

                canidates = ir.initCanidates()
                canidates = updateCanidatesList(solution, canidates )

                numberPruned, canidates = pruneCanidates(canidates)
                numberFilled, solution, dicOfFuncs = fillSolution(solution, canidates, dicOfFuncs )

            numZerosAfterAllFill = sum(x.count(0) for x in solution)
            if  numZerosAfterAllFill in (numZerosBeforeAllFill,0):
                break
            numZerosBeforeAllFill = numZerosAfterAllFill
        # end while loop for this puzzle
        val['end0s'] = numZerosAfterAllFill
        puzzlesDict = updatePuzzlesDictCntrs(puzzlesDict,key, dicOfFuncs)
        val['solution'] = solution
        print(f'{pound62}')
    # end for loop on all puzzles

    pr.printResults(puzzlesDict, 'all')
    pr.printResults(puzzlesDict, 'summary')

    #for key in puzzlesDict:
    #    print()
    #    print(key)
    #    ans = puzzlesDict[key]['solution']
    #    pp.pprint(ans)
    #
    #    print('row sums = ', end = '')
    #    for row in ans:
    #        print(sum(row), ' ', end = '')
    #    print()
    #
    #    Xpos = [[row[i] for row in ans] for i in range(len(ans[0]))]
    #    print('col sums = ', end = '')
    #    for row in Xpos:
    #        print(sum(row), ' ', end = '')
    #    print()
    ##
