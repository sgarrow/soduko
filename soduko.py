# New comment for git2.
import pprint        as pp
import printRoutines as pr
import initRoutines  as ir
import fillRoutines  as fr
import nakedAndHiddenTuples as nht
import xWing as xw
#############################################################################

def findRowsColsInSquare(rIdx, cIdx):
    if rIdx % 3 == 0: rOffsets = [ 1, 2]
    if rIdx % 3 == 1: rOffsets = [-1, 1]
    if rIdx % 3 == 2: rOffsets = [-1,-2] 
    if cIdx % 3 == 0: cOffsets = [ 1, 2]
    if cIdx % 3 == 1: cOffsets = [-1, 1] 
    if cIdx % 3 == 2: cOffsets = [-1,-2] 
    rowsInSquare = [ rIdx+rOffsets[0], rIdx+rOffsets[1] ]
    colsInSquare = [ cIdx+cOffsets[0], cIdx+cOffsets[1] ]
    return rowsInSquare, colsInSquare
#############################################################################

def updateCanidatesList(solution,canidates):
    print('\nUpdating canidates list')
    Xpos = [ [ row[i] for row in solution] for i in range(len(solution[0]))]
    cols = [ x for x in Xpos ] 

    for rIdx,row in enumerate(solution):
        for cIdx,el in enumerate(row):
            prEn = False
            col = cols[cIdx]

            if el != 0:
                canidates[rIdx][cIdx] = 0
            else:
                for ii in [1,2,3,4,5,6,7,8,9]:

                    inRow = True
                    if row.count(ii) == 0: inRow = False

                    inCol = True
                    if col.count(ii) == 0: inCol = False

                    inSquare = False
                    rowsInSquare, colsInSquare = findRowsColsInSquare(rIdx, cIdx)

                    for ris in rowsInSquare:
                        for cis in colsInSquare:
                            if solution[ris][cis] == ii:
                                inSquare = True
                                break
                        if inSquare:
                            break

                    #print('   inRow={}, inCol={}, inSquare={}'.format(inRow, inCol, inSquare))
                    if( not inRow and not inCol and not inSquare):
                        #print('   Adding {} as canidate for {},{}'.format(ii,rIdx,cIdx))
                        if canidates[rIdx][cIdx] != 0: 
                            canidates[rIdx][cIdx].append(ii)
    return canidates
#############################################################################

def updatePuzzlesDictCntrs(puzzlesDict,k,  dicOfFuncs):
    puzzlesDict[k]['oC'] = dicOfFuncs['one']['calls'  ]
    puzzlesDict[k]['oR'] = dicOfFuncs['one']['replace'] 
    puzzlesDict[k]['rC'] = dicOfFuncs['row']['calls'  ] 
    puzzlesDict[k]['rR'] = dicOfFuncs['row']['replace'] 
    puzzlesDict[k]['cC'] = dicOfFuncs['col']['calls'  ] 
    puzzlesDict[k]['cR'] = dicOfFuncs['col']['replace'] 
    puzzlesDict[k]['sC'] = dicOfFuncs['sqr']['calls'  ] 
    puzzlesDict[k]['sR'] = dicOfFuncs['sqr']['replace'] 
    return puzzlesDict
#############################################################################

def prune_NHT(canidates):
    hiddenOrNaked = [ 'hidden', 'naked' ]
    house         = [ 'row','col','sqr' ]
    tupSize       = [4,3,2]
    totNumPruned  = 0

    for hn in hiddenOrNaked:
        for N in tupSize:
            for h in house:
                #print('Pruning {:6} {}-tuples in {}s'.format(hn,N,h))
                numPruned, canidates = nht.pruneNakedAndHiddenTuples(canidates, h, hn, N)
                totNumPruned += numPruned
    
                if numPruned:
                    print('    Prunned {:2} canidates RE: {:6} {}-tuples in {}s'.\
                        format(numPruned, hn,N,h))

    return totNumPruned, canidates
#############################################################################

def prune_XW(canidates):
    totNumPruned = 0
    house = [ 'row','col' ]
    for h in house:
        numPruned, canidates = xw.pruneXwings(canidates, h)
        totNumPruned += numPruned

        if numPruned:
            print('    Prunned {:2} canidates RE: X-Wings in {}s'.\
                format(numPruned, h))

    return totNumPruned, canidates
#############################################################################

def pruneCanidates(canidates):

    print('\nPruning  canidates list')
    totNumPruned_XW  = 0
    totNumPruned_NHT = 0
    passNum_XW       = 0
    passNum_NHT      = 0

    prunedAtLeastOne = True
    while prunedAtLeastOne:
        prunedAtLeastOne = False
        numPruned = 1
        while numPruned:
            print('  prune_XW  pass {}'.format(passNum_XW))
            numPruned, canidates = prune_XW(canidates)
            totNumPruned_XW += numPruned
            print('  prune_XW  prunned {}\n'.format(numPruned))
            passNum_XW += 1
            if numPruned > 0: prunedAtLeastOne = True 
    
        numPruned = 1
        while numPruned:
            print('  prune_NHT pass {}'.format(passNum_NHT))
            numPruned, canidates = prune_NHT(canidates)
            totNumPruned_NHT += numPruned
            print('  prune_NHT  prunned {}\n'.format(numPruned))
            passNum_NHT += 1
            if numPruned > 0: prunedAtLeastOne = True 
        print(31*'*')                     
    
    print('  Total Prunned NHT {:2} {}'.format(totNumPruned_NHT, 39*'*'))
    print('  Total Prunned XW  {:2} {}'.format(totNumPruned_XW,  39*'*'))
    print(62*'*')                     
    return totNumPruned_XW + totNumPruned_NHT, canidates
#############################################################################

def fillSolution(solution, canidates, dicOfFuncs ):
    totalNumFilled = 0

    print('\nFilling in solution cells')
    for k in dicOfFuncs:
        numFilled, solution = dicOfFuncs[k]['func']( solution, canidates )
        totalNumFilled  += numFilled
        dicOfFuncs[k]['calls']   += 1
        dicOfFuncs[k]['replace'] += numFilled
    print('\n  Total filled {:2d} {}'.format(totalNumFilled, 44*'*'))
    print(62*'*')                     

    return totalNumFilled, solution, dicOfFuncs
#############################################################################

if __name__ == '__main__':
    from puzzles import puzzlesDict

    dicOfFuncs = {
        'one': { 'func': fr.fillCellsVia_1_Canidate, 'calls': 0, 'replace': 0 },
        'row': { 'func': fr.fillCellsViaRowHistAnal, 'calls': 0, 'replace': 0 },  
        'col': { 'func': fr.fillCellsViaColHistAnal, 'calls': 0, 'replace': 0 },  
        'sqr': { 'func': fr.fillCellsViaSqrHistAnal, 'calls': 0, 'replace': 0 }}

    for key in puzzlesDict:
        print('Processing puzzle {}'.format(key))
        solution = [x[:] for x in puzzlesDict[key]['puzzle'] ]
        puzzlesDict[key]['start0s'] = sum(x.count(0) for x in solution)
        dicOfFuncs = ir.initDicOfFuncsCntrs(dicOfFuncs)
        while (1):
            numZerosBeforeAllFill = sum(x.count(0) for x in solution)
            if sum(x.count(0) for x in solution)==0: break
            numFilled = 1
            while (numFilled):

                if sum(x.count(0) for x in solution)==0: break

                canidates = ir.initCanidates()
                canidates = updateCanidatesList(solution, canidates )

                numPruned, canidates = pruneCanidates(canidates)
                numFilled, solution, dicOfFuncs = fillSolution(solution, canidates, dicOfFuncs )
                 
            numZerosAfterAllFill = sum(x.count(0) for x in solution)
            if  numZerosAfterAllFill == numZerosBeforeAllFill or \
                numZerosAfterAllFill == 0: 
                break
            else: 
                numZerosBeforeAllFill = numZerosAfterAllFill
        # end while loop for this puzzle
        puzzlesDict[key]['end0s'] = numZerosAfterAllFill
        puzzlesDict = updatePuzzlesDictCntrs(puzzlesDict,key, dicOfFuncs)
        puzzlesDict[key]['solution'] = solution
        print('{}'.format(62*'#'))
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
