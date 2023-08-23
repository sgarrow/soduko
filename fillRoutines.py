def flatten(x):
    y = []
    for el in x:
        try:
            for subEl in el:
                y.append(subEl)
        except:
            y.append(el)
    return y
#############################################################################

def genHistogram(inLst):
    hist = []
    for bin in range(min(inLst), max(inLst)+1):
        binHeight = len([1 for x in inLst if x==bin])
        if binHeight > 0:
            hist.append((bin, binHeight))
    return hist
#############################################################################

def fillCellsVia_1_Canidate(solution, canidates):
    print('\n  Filling solution cells that have only 1 canidate')
    numFilled = 0
    for rIdx,row in enumerate(solution):
        for cIdx,el in enumerate(row):
            if canidates[rIdx][cIdx] != 0 and len(canidates[rIdx][cIdx]) == 1:
                if solution[rIdx][cIdx] == 0:
                    print('    Placing {} at {},{}'.\
                        format(canidates[rIdx][cIdx][0], rIdx,cIdx ), end='')
                    solution[rIdx][cIdx] = canidates[rIdx][cIdx][0]
                    numFilled += 1
                    if numFilled%3 == 0: print()
    if numFilled != 0:
        print('\n    NumZeros = {}.'.format(sum(x.count(0) for x in solution) ))
    return numFilled,solution
#############################################################################

def fillCellsViaRowHistAnal(solution, canidates):
    print('\n  Filling solution cells thru Row Hist Analysis')
    numFilled = 0

    for r,row in enumerate(canidates):

        flatRow = flatten(row)
        histRow = genHistogram(flatRow)
        binsHeightOne = [ x[0] for x in histRow if x[1] == 1 and x[0] != 0]

        if len(binsHeightOne) > 0:
            valOfBinHeight1 = binsHeightOne[0]
            subListContainingThatVal = \
                [ x for x in row if x != 0 and valOfBinHeight1 in x]
            idxOfSubLst =  row.index(subListContainingThatVal[0])
            if solution[r][idxOfSubLst] == 0:
                print('    Placing {} at {},{}'.format(valOfBinHeight1,r,idxOfSubLst))
                solution[r][idxOfSubLst] = valOfBinHeight1
                numFilled += 1
    if numFilled != 0:
        print('    NumZeros = {}.'.format(sum(x.count(0) for x in solution) ))
    return numFilled,solution
#############################################################################

def fillCellsViaColHistAnal(solution, canidates):
    print('\n  Filling solution cells thru Col Hist Analysis')
    numFilled = 0
    Xpos = [[row[i] for row in canidates] for i in range(len(canidates[0]))]

    for c,col in enumerate(Xpos):

        flatCol = flatten(col)
        histCol = genHistogram(flatCol)
        binsHeightOne = [ x[0] for x in histCol if x[1] == 1 and x[0] != 0]

        if len(binsHeightOne) > 0:
            valOfBinHeight1 = binsHeightOne[0]
            subListContainingThatVal = \
                [ x for x in col if x != 0 and valOfBinHeight1 in x]
            idxOfSubLst =  col.index(subListContainingThatVal[0])
            if solution[idxOfSubLst][c] == 0:
                print('    Placing {} at {},{}'.format(valOfBinHeight1,idxOfSubLst,c))
                solution[idxOfSubLst][c] = valOfBinHeight1
                numFilled += 1
    if numFilled != 0:
        print('    NumZeros = {}.'.format(sum(x.count(0) for x in solution) ))
    return numFilled,solution
#############################################################################

def fillCellsViaSqrHistAnal(solution, canidates):
    print('\n  Filling solution cells thru Sqr Hist Analysis')
    numFilled = 0
    squareNums = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]] 

    for squareNum in squareNums:
        rowsInSq = [ x+squareNum[0]*3 for x in [0,1,2] ]
        colsInSq = [ x+squareNum[1]*3 for x in [0,1,2] ]

        coordsInSq = [ [r,c] for r in rowsInSq for c in colsInSq ]
        canidatesSq = [ canidates[x[0]][x[1]] for x in coordsInSq ] 

        flatSq = flatten(canidatesSq)
        histSq = genHistogram(flatSq)
        binsHeightOne = [ x[0] for x in histSq if x[1] == 1 and x[0] != 0]

        if len(binsHeightOne) > 0:
            valOfBinHeight1 = binsHeightOne[0]
            subListContainingThatVal = \
                [ x for x in canidatesSq if x != 0 and valOfBinHeight1 in x]
            idxOfSubLst =  canidatesSq.index(subListContainingThatVal[0])
            r = rowsInSq[(idxOfSubLst // 3)]
            c = colsInSq[(idxOfSubLst %  3)]

            if solution[r][c] == 0:
                print('    Placing {} at {},{}'.format(valOfBinHeight1, r, c ))
                solution[r][c] = valOfBinHeight1
                numFilled += 1
    if numFilled != 0:
        print('    NumZeros = {}.'.format(sum(x.count(0) for x in solution) ))
    return numFilled,solution
#############################################################################


