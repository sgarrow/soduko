#import printRoutines as pr
import copy
import pprint  as pp
import mapping as mp
import printRoutines as pr
#############################################################################

def flatten(inLst):
    outLst = []
    for elem in inLst:
        try:
            for subEl in elem:
                outLst.append(subEl)
        except TypeError:
            outLst.append(elem)
    return outLst
#############################################################################

def genHistogram(inLst):
    hist = []
    for histBin in range(min(inLst), max(inLst)+1):
        binHeight = len([1 for x in inLst if x==histBin])
        if binHeight > 0:
            hist.append((histBin, binHeight))
    return hist
#############################################################################

def fillViaOneCanidate(solution, canidates, lclPrintDic, house):
    if lclPrintDic['flPrn'] >= 1:
        print('\n  Filling solution cells that have only 1 canidate')
    numFilled = 0
    for rIdx,row in enumerate(solution):
        for cIdx in range(len(row)):
            if canidates[rIdx][cIdx] != 0 and len(canidates[rIdx][cIdx])==1:
                if solution[rIdx][cIdx] == 0:
                    if lclPrintDic['flPrn'] >= 2:
                        print(f'    Placing {canidates[rIdx][cIdx][0]} at {rIdx},{cIdx}', end = '')
                    solution[rIdx][cIdx] = canidates[rIdx][cIdx][0]
                    numFilled += 1
                    if lclPrintDic['flPrn'] >= 2:
                        if numFilled%3 == 0:
                            print()
    numZeros = sum(x.count(0) for x in solution)
    if lclPrintDic['flPrn'] >= 1:
        print(f'    numFilled = {numFilled}. NumZeros = {numZeros}.\n')
    return numFilled,solution
#############################################################################

def fillViaRCHistAnal(lclSolution, lclCanidates, lclPrintDic, house):

    if lclPrintDic['flPrn'] >= 1:
        print('  Filling solution cells thru {} Hist Analysis'.format(house))

    cpyDic = {'row':copy.deepcopy, 'col':mp.mapColsToRows, 'sqr':mp.mapSrqsToRows}
    xCanidates = cpyDic[house](lclCanidates)

    #pr.printCanidates(lclCanidates,  alreadyPrn = False)
    #pr.printCanidates(xCanidates, alreadyPrn = False)

    numFilled = 0
    for rc_Idx,rowOrCol in enumerate(xCanidates):

        flatRow            = flatten(rowOrCol)
        valsOfCntOne       = []
        idxsOfValsOfCntOne = []
        for val in range(1,10):
            cntThisVal = flatRow.count(val)

            if cntThisVal == 1:
                valsOfCntOne.append(val)

                idxsOfValsOfCntOne.\
                append([ii for ii,cans in enumerate(rowOrCol)\
                if cans !=0 and val in cans][0])

        #print('rowOrCol           ', rowOrCol)
        #print('\nvalsOfCntOne       ', valsOfCntOne)
        #print('idxsOfValsOfCntOne ', idxsOfValsOfCntOne)

        for idx,val in zip(idxsOfValsOfCntOne,valsOfCntOne):
            #print(idx,val)

            if house == 'row':
                if lclSolution[rc_Idx][idx] == 0:
                    if lclPrintDic['flPrn'] >= 2:
                        print(f'    Placing {val} at {rc_Idx},{idx}')
                    lclSolution[rc_Idx][idx] = val
                    numFilled += 1

            if house == 'col':
                if lclSolution[idx][rc_Idx] == 0:
                    if lclPrintDic['flPrn'] >= 2:
                        print(f'    Placing {val} at {idx},{rc_Idx}') 
                    lclSolution[idx][rc_Idx] = val
                    numFilled += 1

    numZeros = sum(x.count(0) for x in lclSolution)
    if lclPrintDic['flPrn'] >= 1:
        print(f'    numFilled = {numFilled}. NumZeros = {numZeros}.\n')

    cpyDic = {'row':copy.deepcopy, 'col':mp.mapRowsToCols, 'sqr':mp.mapRowsToSqrs}
    canidates = cpyDic[house](xCanidates)

    #input()
    return numFilled,lclSolution
#############################################################################

def fillViaSqrHistAnal(solution, lclCanidates, lclPrintDic,house):
    if lclPrintDic['flPrn'] >= 1:
        print('  Filling solution cells thru Sqr Hist Analysis')
    numFilled = 0
    squareNums = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]

    for squareNum in squareNums:
        rowsInSq = [ x+squareNum[0]*3 for x in [0,1,2] ]
        colsInSq = [ x+squareNum[1]*3 for x in [0,1,2] ]

        coordsInSq = [ [row,col] for row in rowsInSq for col in colsInSq ]
        canidatesSq = [ lclCanidates[x[0]][x[1]] for x in coordsInSq ]

        flatSq = flatten(canidatesSq)
        histSq = genHistogram(flatSq)
        binsHeightOne = [ x[0] for x in histSq if x[1] == 1 and x[0] != 0]

        if len(binsHeightOne) > 0:
            valOfBinHeight1 = binsHeightOne[0]
            subListContainingThatVal = \
                [ x for x in canidatesSq if x != 0 and valOfBinHeight1 in x]
            idxOfSubLst =  canidatesSq.index(subListContainingThatVal[0])
            row = rowsInSq[(idxOfSubLst // 3)]
            col = colsInSq[(idxOfSubLst %  3)]

            if solution[row][col] == 0:
                if lclPrintDic['flPrn'] >= 2:
                    print(f'    Placing {valOfBinHeight1} at {row},{col}')
                solution[row][col] = valOfBinHeight1
                numFilled += 1
    numZeros = sum(x.count(0) for x in solution)
    if lclPrintDic['flPrn'] >= 1:
        print(f'    numFilled = {numFilled}. NumZeros = {numZeros}.\n')
    return numFilled,solution
#############################################################################
