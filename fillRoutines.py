import copy
import utils as ut
#############################################################################

def fillViaOneCanidate(solution, canidates, cfgDic, house):
    if house:
        pass # Unused arg warning.

    numFilled = 0

    placedStr = ''
    for rIdx,row in enumerate(solution):
        for cIdx in range(len(row)):

            if  canidates[rIdx][cIdx]      != 0  and \
                len(canidates[rIdx][cIdx]) == 1  and \
                solution[rIdx][cIdx]       == 0:

                solution[rIdx][cIdx] = canidates[rIdx][cIdx][0]
                numFilled += 1

                placedStr += '    {} at {},{}'.\
                    format(canidates[rIdx][cIdx][0],rIdx,cIdx, end = '')
                if numFilled%5 == 0: placedStr += '\n'

    if numFilled%5 != 0: placedStr += '\n' 
    numZeros = sum(x.count(0) for x in solution)

    if cfgDic['fill']['prnLevel'] >= 1:
        print('  Cells filled RE: one canidate : {:2} ({:2} unfilled cells left)'.format(numFilled, numZeros))
    if cfgDic['fill']['prnLevel'] >= 2:
        print(placedStr)

    return numFilled,solution
#############################################################################

def fillViaRCHistAnal(lclSolution, lclCanidates, cfgDic, house):
    cpyDic={'row':copy.deepcopy,'col':ut.mapColsToRows,'sqr':ut.mapSrqsToRows}
    xCanidates = cpyDic[house](lclCanidates)
    numFilled  = 0

    placedStr = ''
    for rcsIdx,rowColOrSqr in enumerate(xCanidates):

        flatRow            = ut.flatten(rowColOrSqr)
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

            rIdx,cIdx = 0,0
            if house == 'row': rIdx,cIdx = rcsIdx,idx
            if house == 'col': rIdx,cIdx = idx, rcsIdx
            if house == 'sqr': rIdx,cIdx = ut.getRowColFromSqrOffset(rcsIdx,idx)

            if lclSolution[rIdx][cIdx] == 0:
                lclSolution[rIdx][cIdx] = val
                numFilled += 1
                placedStr += '    {} at {},{}'.format(val,rIdx,cIdx, end = '')
                if numFilled%5 == 0: placedStr += '\n'

    if numFilled%5 != 0: placedStr += '\n' 
    numZeros = sum(x.count(0) for x in lclSolution)

    if cfgDic['fill']['prnLevel'] >= 1:
        print('  Cells filled RE: {} histogram: {:2} ({:2} unfilled cells left)'.format(house, numFilled, numZeros))
    if cfgDic['fill']['prnLevel'] >= 2:
        print(placedStr)

    return numFilled,lclSolution
#############################################################################
