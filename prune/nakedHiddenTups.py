from itertools import combinations
import copy          as cp
import pprint        as pp
import printRoutines as pr
import mapping       as mp
############################################################################

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
    cpyDic = {'row':cp.deepcopy, 'col':mp.mapColsToRows, 'sqr':mp.mapSrqsToRows}
    xCanidates = cpyDic[house](canidates)

    numPruned = 0
    for idx, rowOrColOrSqrWithZeros in enumerate(xCanidates):
        rOrCOrS = [set(x) if x != 0 else set([0]) for x in rowOrColOrSqrWithZeros]
        combSet = combinations(rOrCOrS, tupSiz)  # C(n,r) = n! / ( r! * (n-r)! ). C(9,3)=84.
        combIdxs = getComIdxs(rOrCOrS, tupSiz)

        for comb,comIdx in zip(combSet,combIdxs):
            if any(el == {0} for el in comb) or any(len(el) == 1 for el in comb):
                continue

            comIdxC = [ x for x in range(0,len(rOrCOrS)) if x not in comIdx ]
            setH    = set.union(*comb)
            setG    = set(flatten([ rOrCOrS[ii] for ii in comIdxC if rOrCOrS[ii] != [0]]))
            lstHmG  = list(setH - setG)

            hIsNaked = len(setH) == tupSiz

            hIsHidden = False
            if (len(setH) > tupSiz) and (len(lstHmG) == tupSiz):
                hIsHidden = True
                for aComb in comb:
                    if len(set.intersection(set(lstHmG), aComb) ) == 0:
                        hIsHidden = False
                        break

            if hIsHidden and hiddenOrNaked == 'hidden':
                myD = {'row': idx, 'tripVals': lstHmG, 'tripIdxs': comIdx }
                if lclPrintDic['nhPrn'] >= 1:
                    myDstr = pp.pformat(myD)
                    print('\n   Hidden ({}) \n      {}'.format(house, myDstr))

                alreadyPrinted = False
                for tripIdx in myD['tripIdxs']:
                    temp  = [ x for x in rOrCOrS[tripIdx] if x in myD['tripVals'] ]
                    diff  = set(rOrCOrS[tripIdx]) - set.intersection( rOrCOrS[tripIdx], set(temp) )
                    if len(diff) != 0:
                        numPruned += len(diff)
                        if lclPrintDic['nhPrn'] >= 2:
                            pr.printCanidates(xCanidates, alreadyPrn = alreadyPrinted)
                            alreadyPrinted = True
                        if lclPrintDic['nhPrn'] >= 1:
                            print( '        remove {:>8} from ({},{})'.\
                                format(str(diff),myD['row'],tripIdx))

                    xCanidates[myD['row']][tripIdx] = temp
                break

            if hIsNaked and hiddenOrNaked == 'naked':
                myD   = {'row': idx, 'tripVals': setH, 'tripIdxs': comIdx }
                if lclPrintDic['nhPrn'] >= 1:
                    myDstr = pp.pformat(myD)
                    print('\n   Naked ({}) \n      {}'.format(house, myDstr))

                temp  = [ list(x) if kk in myD['tripIdxs'] else \
                          list(x-myD['tripVals']) for kk,x in enumerate(rOrCOrS) ]
                temp2 = [ x if x != [0] else 0 for x in temp]

                alreadyPrinted = False
                for idx, elem in enumerate(rOrCOrS):
                    diff  = elem - set.intersection( elem, set(temp[idx]) )
                    if len(diff) != 0:
                        numPruned += len(diff)
                        if lclPrintDic['nhPrn'] >= 2:
                            pr.printCanidates(xCanidates, alreadyPrn = alreadyPrinted)
                            alreadyPrinted = True
                        if lclPrintDic['nhPrn'] >= 1:
                            print( '        remove {:>8} from ({},{})'.\
                                format(str(diff), myD['row'], idx) )

                xCanidates[myD['row']] = temp2
                break

    cpyDic = {'row':cp.deepcopy, 'col':mp.mapRowsToCols, 'sqr':mp.mapRowsToSqrs}
    canidates = cpyDic[house](xCanidates)

    return(numPruned, canidates)
############################################################################
