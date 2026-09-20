from itertools import combinations
import copy          as cp
import pprint        as pp

import printRoutines as pr
import utils         as ut
############################################################################

def getComIdxs(rOrCOrS, tupSiz):
    combIdxs = 0
    if tupSiz == 2:
        combIdxs = \
        list((i,j) for ((i,_),(j,_)) in \
        combinations(enumerate(rOrCOrS), tupSiz))
    elif tupSiz == 3:
        combIdxs = \
        list((i,j,k) for ((i,_),(j,_),(k,_)) in \
        combinations(enumerate(rOrCOrS), tupSiz))
    elif tupSiz == 4:
        combIdxs = \
        list((i,j,k,l) for ((i,_),(j,_),(k,_),(l,_)) in \
        combinations(enumerate(rOrCOrS), tupSiz))
    elif tupSiz == 5:
        combIdxs = \
        list((i,j,k,l,m) for ((i,_),(j,_),(k,_),(l,_),(m,_)) in \
        combinations(enumerate(rOrCOrS), tupSiz))
    return combIdxs
############################################################################

def pruneNakedAndHiddenTuples(canidates, house, hiddenOrNaked, tupSiz, lclPrintDic):
    cpyDic = {'row':cp.deepcopy, 'col':ut.mapColsToRows, 'sqr':ut.mapSrqsToRows}
    xCanidates = cpyDic[house](canidates)

    numPruned = 0
    for idx, rowOrColOrSqrWithZeros in enumerate(xCanidates):

        colorCordAndValDict = {}

        rOrCOrS = [set(x) if x != 0 else set([0]) for x in rowOrColOrSqrWithZeros]
        combSet = combinations(rOrCOrS, tupSiz)  # C(n,r) = n! / ( r! * (n-r)! ). C(9,3)=84.
        combIdxs = getComIdxs(rOrCOrS, tupSiz)

        for comb,comIdx in zip(combSet,combIdxs):
            if any(el == {0} for el in comb) or any(len(el) == 1 for el in comb):
                continue

            comIdxC = [ x for x in range(0,len(rOrCOrS)) if x not in comIdx ]
            setH    = set.union(*comb)
            setG    = set(ut.flatten([ rOrCOrS[ii] for ii in comIdxC if rOrCOrS[ii] != [0]]))
            lstHmG  = list(setH - setG)

            hIsNaked  = len(setH) == tupSiz
            hIsHidden = False
            if (len(setH) > tupSiz) and (len(lstHmG) == tupSiz):
                hIsHidden = True
                for aComb in comb:
                    if len(set.intersection(set(lstHmG), aComb) ) == 0:
                        hIsHidden = False
                        break

            noRemoveStr = '        Nothing to remove'
            removeStr   = noRemoveStr

            if hIsHidden and hiddenOrNaked == 'hidden':
                # Process a naked tuple in this single row (or col or square).
                myD = {'row': idx, 'tripVals': lstHmG, 'tripIdxs': comIdx }

                for tripIdx in myD['tripIdxs']:
                    for val in myD['tripVals']:
                        colorCordAndValDict[len(colorCordAndValDict)] = \
                            {'GRN': {'coord': [myD['row'], tripIdx], 'val': val}}

                for tripIdx in myD['tripIdxs']:
                    temp  = [ x for x in rOrCOrS[tripIdx] if x in myD['tripVals'] ]
                    diff  = set(rOrCOrS[tripIdx]) - set.intersection( rOrCOrS[tripIdx], set(temp) )

                    if len(diff) != 0:
                        removeStr = ''
                        numPruned += len(diff)

                        for ii in range(len(diff)):
                            colorCordAndValDict[len(colorCordAndValDict)] = \
                            { 'RED': { 'coord' : [myD['row'], tripIdx],
                                       'val'   : list(diff)[ii] }}

                        removeStr += '        remove {:>8} from ({},{})'.\
                            format(str(diff),myD['row'],tripIdx)

                    if lclPrintDic['nhPrn'] >= 1:
                        print('\n   Hidden {}-tuple in {} \n      {}'.\
                            format(tupSiz, house, pp.pformat(myD)))
                        print(removeStr)
    
                    if lclPrintDic['nhPrn'] >= 2 and removeStr != noRemoveStr:
                        pr.printCanidates(xCanidates, colorCordAndValDict)

                    xCanidates[myD['row']][tripIdx] = temp # Now actually remove them.
                break

            if hIsNaked and hiddenOrNaked == 'naked':
                # Process a naked tuple in this single row (or col or square).
                myD   = {'row': idx, 'tripVals': setH, 'tripIdxs': comIdx }

                for tripIdx in myD['tripIdxs']:
                    for val in myD['tripVals']:
                        colorCordAndValDict[len(colorCordAndValDict)] = \
                            {'GRN': {'coord': [myD['row'], tripIdx], 'val': val}}

                temp  = [ list(x) if kk in myD['tripIdxs'] else \
                          list(x-myD['tripVals']) for kk,x in enumerate(rOrCOrS) ]
                temp2 = [ x if x != [0] else 0 for x in temp]

                for idx, elem in enumerate(rOrCOrS):
                    diff  = elem - set.intersection( elem, set(temp[idx]) )

                    if len(diff) != 0:
                        removeStr = ''
                        numPruned += len(diff)
                        for ii in range(len(diff)):
                            colorCordAndValDict[len(colorCordAndValDict)] = \
                            { 'RED': { 'coord': [myD['row'], idx],
                                       'val': list(diff)[ii] }}

                        removeStr += '        remove {:>8} from ({},{})'.\
                            format(str(diff), myD['row'], idx)

                if lclPrintDic['nhPrn'] >= 1:
                    print('\n   Naked {}-tuple in {} \n      {}'.\
                        format(tupSiz, house, pp.pformat(myD)))
                    print(removeStr)

                if lclPrintDic['nhPrn'] >= 2 and removeStr != noRemoveStr:
                    pr.printCanidates(xCanidates, colorCordAndValDict)

                xCanidates[myD['row']] = temp2 # Now actually remove them.
                break

    cpyDic = {'row':cp.deepcopy, 'col':ut.mapRowsToCols, 'sqr':ut.mapRowsToSqrs}
    canidates = cpyDic[house](xCanidates)

    return(numPruned, canidates)
############################################################################
