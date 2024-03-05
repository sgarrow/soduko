#import printRoutines as pr

NEWLINE = '\n'
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

def fillViaOneCanidate(solution, canidates, lclPrintDic):
    if lclPrintDic['flPrn'] >= 1:
        print('\n  Filling solution cells that have only 1 canidate')
    numFilled = 0
    for rIdx,row in enumerate(solution):
        for cIdx in range(len(row)):
            if canidates[rIdx][cIdx] != 0 and len(canidates[rIdx][cIdx]) == 1:
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

def fillViaRowHistAnal(solution, canidates, lclPrintDic):
    if lclPrintDic['flPrn'] >= 1:
        print('  Filling solution cells thru Row Hist Analysis')
    numFilled = 0

    for rIdx,row in enumerate(canidates):

        flatRow = flatten(row)
        histRow = genHistogram(flatRow)
        binsHeightOne = [ x[0] for x in histRow if x[1] == 1 and x[0] != 0]

        if len(binsHeightOne) > 0:
            valOfBinHeight1 = binsHeightOne[0]
            subListContainingThatVal = \
                [ x for x in row if x != 0 and valOfBinHeight1 in x]
            idxOfSubLst =  row.index(subListContainingThatVal[0])
            if solution[rIdx][idxOfSubLst] == 0:
                if lclPrintDic['flPrn'] >= 2:
                    print(f'    Placing {valOfBinHeight1} at {rIdx},{idxOfSubLst}')
                solution[rIdx][idxOfSubLst] = valOfBinHeight1
                numFilled += 1
    numZeros = sum(x.count(0) for x in solution)
    if lclPrintDic['flPrn'] >= 1:
        print(f'    numFilled = {numFilled}. NumZeros = {numZeros}.\n')
    return numFilled,solution
#############################################################################

def fillViaColHistAnal(solution, canidates, lclPrintDic):
    if lclPrintDic['flPrn'] >= 1:
        print('  Filling solution cells thru Col Hist Analysis')
    numFilled = 0
    xPos = [[row[i] for row in canidates] for i in range(len(canidates[0]))]

    for cIdx,col in enumerate(xPos):

        flatCol = flatten(col)
        histCol = genHistogram(flatCol)
        binsHeightOne = [ x[0] for x in histCol if x[1] == 1 and x[0] != 0]

        if len(binsHeightOne) > 0:
            valOfBinHeight1 = binsHeightOne[0]
            subListContainingThatVal = \
                [ x for x in col if x != 0 and valOfBinHeight1 in x]
            idxOfSubLst =  col.index(subListContainingThatVal[0])
            if solution[idxOfSubLst][cIdx] == 0:
                if lclPrintDic['flPrn'] >= 2:
                    print(f'    Placing {valOfBinHeight1} at {idxOfSubLst},{cIdx}')
                solution[idxOfSubLst][cIdx] = valOfBinHeight1
                numFilled += 1
    numZeros = sum(x.count(0) for x in solution)
    if lclPrintDic['flPrn'] >= 1:
        print(f'    numFilled = {numFilled}. NumZeros = {numZeros}.\n')
    return numFilled,solution
#############################################################################

def fillViaSqrHistAnal(solution, canidates, lclPrintDic):
    if lclPrintDic['flPrn'] >= 1:
        print('  Filling solution cells thru Sqr Hist Analysis')
    numFilled = 0
    squareNums = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]

    for squareNum in squareNums:
        rowsInSq = [ x+squareNum[0]*3 for x in [0,1,2] ]
        colsInSq = [ x+squareNum[1]*3 for x in [0,1,2] ]

        coordsInSq = [ [row,col] for row in rowsInSq for col in colsInSq ]
        canidatesSq = [ canidates[x[0]][x[1]] for x in coordsInSq ]

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
