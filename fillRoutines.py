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
    if numFilled%3 != 0: print()
    numZeros = sum(x.count(0) for x in solution)
    if lclPrintDic['flPrn'] >= 1:
        print(f'  numFilled = {numFilled}. NumZeros = {numZeros}.\n')
    return numFilled,solution
#############################################################################

def fillViaRCHistAnal(lclSolution, lclCanidates, lclPrintDic, house):

    if lclPrintDic['flPrn'] >= 1:
        print('  Filling solution cells thru {} Hist Analysis'.format(house))

    cpyDic = {'row':copy.deepcopy, 'col':mp.mapColsToRows, 'sqr':mp.mapSrqsToRows}
    xCanidates = cpyDic[house](lclCanidates)

    numFilled = 0
    for rcs_Idx,rowColOrSqr in enumerate(xCanidates):

        flatRow            = flatten(rowColOrSqr)
        valsOfCntOne       = []
        idxsOfValsOfCntOne = []
        for val in range(1,10):
            cntThisVal = flatRow.count(val)

            if cntThisVal == 1:
                valsOfCntOne.append(val)

                idxsOfValsOfCntOne.\
                append([ii for ii,cans in enumerate(rowColOrSqr)\
                if cans !=0 and val in cans][0])

        for idx,val in zip(idxsOfValsOfCntOne,valsOfCntOne):

            if house == 'row': rIdx,cIdx = rcs_Idx,idx
            if house == 'col': rIdx,cIdx = idx, rcs_Idx
            if house == 'sqr': rIdx,cIdx = mp.getRowColFromSqrOffset(rcs_Idx,idx)

            if lclSolution[rIdx][cIdx] == 0:
                if lclPrintDic['flPrn'] >= 2:
                    print(f'    Placing {val} at {rIdx},{cIdx}', end = '')
                lclSolution[rIdx][cIdx] = val
                numFilled += 1
                if lclPrintDic['flPrn'] >= 2:
                    if numFilled%3 == 0:
                        print()

    if numFilled%3 != 0: print()
    numZeros = sum(x.count(0) for x in lclSolution)
    if lclPrintDic['flPrn'] >= 1:
        print(f'  numFilled = {numFilled}. NumZeros = {numZeros}.\n')

    return numFilled,lclSolution
#############################################################################
