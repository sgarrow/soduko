# New comment for git2.
import pprint        as pp
import printRoutines as pr
import initRoutines  as ir
import fillRoutines  as fr
import nakedPairs    as np
import nakedTriples  as nt
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
            for k in dicOfFuncs:
                if sum(x.count(0) for x in solution)==0: break
                numFilled = 1
                while (numFilled):
                    if sum(x.count(0) for x in solution)==0: break
                    canidates = ir.initCanidates()
                    canidates = updateCanidatesList(solution, canidates)

                    numPruned1 = 1
                    numPruned2 = 1
                    while numPruned1 or numPruned2:
                       numPruned1, canidates = np.pruneNakedPairs(canidates)
                       numPruned2, canidates = nt.pruneNakedTriples(canidates)

                    numFilled, solution = dicOfFuncs[k]['func']( solution, canidates )
                    dicOfFuncs[k]['calls']   += 1
                    dicOfFuncs[k]['replace'] += numFilled
                    if  numFilled == 0: break
                # end while loop on a single fill function
            # end for loop on all fill functions
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

    #pr.printResults(puzzlesDict, 'all')
    pr.printResults(puzzlesDict, 'summary')
    pr.prettyPrint3DArray(canidates)

