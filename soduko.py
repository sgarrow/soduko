# New comment for git2.
import pprint        as pp
import printRoutines as pr
import initRoutines  as ir
import fillRoutines  as fr
import nakedAndHiddenTuples as nht
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

def pruneCanidates(canidates):

    hiddenOrNaked   = [ 'hidden', 'naked' ]
    house           = [ 'row','col','sqr' ]
    tupSize         = [4,3,2]
    totNumPruned = 0

    prunnedAtLeastOne = True
    while prunnedAtLeastOne:
        prunnedAtLeastOne = False
        for hn in ['hidden', 'naked']:
            for N in tupSize:
                for h in house:
    
                    print('Pruning {:6} {}-tuples in {}s'.format(hn,N,h))
    
                    loopNumPruned = 0
                    callNumPruned = 1
                    while callNumPruned:
                        callNumPruned, canidates = nht.pruneHiddenTriples(canidates, h, hn, N)
                        loopNumPruned += callNumPruned
                        totNumPruned  += callNumPruned
                        if callNumPruned != 0:
                            prunnedAtLeastOne = True
    
                    if loopNumPruned:
                        print('Prunned {} {} {}-tuples in {}s\n'.format(loopNumPruned, hn,N,h))
    
        print('********************************************************************************\n')                     

    print('********************************************************************************')                     
    print('Total Prunned {} ***************************************************************'.format(totNumPruned))
    print('********************************************************************************\n')                   

    return totNumPruned, canidates
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
    pr.prettyPrint3DArray(canidates)

