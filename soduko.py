# New comment for git2.
import pprint        as pp
import printRoutines as pr
import initRoutines  as ir
import fillRoutines  as fr
import nakedPairs    as np
import hiddenPairs   as hp
import nakedTriples  as nt
import hiddenTriples as ht
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
                    rowsInSquare, colsInSquare = np.findRowsColsInSquare(rIdx, cIdx)

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

def pruneCanidates(canidates):

    totNumPruned  = 0
    loopNumPruned = 1
    while loopNumPruned:
        loopNumPruned, canidates = ht.pruneHiddenTriplesRowOrCols(canidates, 'row')
        totNumPruned  += loopNumPruned
    print('Total Pruning hidden triples ** ( total pruned =  {} ) ******* End.'.format(totNumPruned))


    numPruned1 = 1
    numPruned2 = 1
    numPruned3 = 1
    while numPruned1 or numPruned2 or numPruned3:
       numPruned1, canidates = np.pruneNakedPairs(canidates)
       numPruned2, canidates = nt.pruneNakedTriples(canidates)
       numPruned3, canidates = hp.pruneHiddenPairs(canidates)
    return numPruned1+numPruned2+numPruned3, canidates
#############################################################################

def fillSolution(solution, canidates, dicOfFuncs ):
    totalNumFilled = 0

    print('\nFilling in solution cells ****************************** Start')
    for k in dicOfFuncs:
        numFilled, solution = dicOfFuncs[k]['func']( solution, canidates )
        totalNumFilled  += numFilled
        dicOfFuncs[k]['calls']   += 1
        dicOfFuncs[k]['replace'] += numFilled
    print('Filling in solution cells ** ( total filled = {:2d} ) ******* End'.
        format(totalNumFilled))

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
        print(' Processing puzzle {}'.format(key))
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
        print('**********************************')
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
    #
    #
    #pr.prettyPrint3DArray(canidates)

