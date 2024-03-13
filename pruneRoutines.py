import copy
from itertools import combinations
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

def genHistogram(inLst):
    hist = []
    for histBin in range(min(inLst), max(inLst)+1):
        binHeight = len([1 for x in inLst if x==histBin])
        if binHeight > 0:
            hist.append((histBin, binHeight))
    return hist
#############################################################################

def getComIdxs(rOrCOrS, tupSiz):
    if tupSiz == 2:
        combIdxs = \
        list((i,j) for ((i,_),(j,_)) in combinations(enumerate(rOrCOrS), tupSiz))
    elif tupSiz == 3:
        combIdxs = \
        list((i,j,k) for ((i,_),(j,_),(k,_)) in combinations(enumerate(rOrCOrS), tupSiz))
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
    cpyDic = {'row':copy.deepcopy, 'col':mp.mapColsToRows, 'sqr':mp.mapSrqsToRows}
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
                            print( '        remove {:>8} from ({},{})'.format(str(diff),myD['row'],tripIdx))

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
                            print( '        remove {:>8} from ({},{})'.format(str(diff), myD['row'], idx) )

                xCanidates[myD['row']] = temp2
                break

    cpyDic = {'row':copy.deepcopy, 'col':mp.mapRowsToCols, 'sqr':mp.mapRowsToSqrs}
    canidates = cpyDic[house](xCanidates)

    return(numPruned, canidates)
############################################################################

def pruneXwings(canidates, house, lclPrintDic):
    cpyDic = {'row':copy.deepcopy, 'col':mp.mapColsToRows, 'sqr':mp.mapSrqsToRows}
    xCanidates = cpyDic[house](canidates)

    numPruned = 0

    allBinsHeightTwo = []
    for row in xCanidates:
        flatRow = flatten(row)
        histRow = genHistogram(flatRow)
        allBinsHeightTwo.append([ x[0] for x in histRow if x[1] == 2 and x[0] != 0])
    #pp.pprint(allBinsHeightTwo)

    k = 0
    myD = {}
    for idx,lstOfVals in enumerate(allBinsHeightTwo):
        for val in lstOfVals:
            cols = [ c for c,lst in enumerate(xCanidates[idx]) if lst != 0 and val in lst ]
            #print(' in row {}, {} appears exactly twice - cols {}'.format(idx, val, cols))
            myD[k] = { 'A_row':idx, 'B_cols':cols, 'C_val':val,  }
            k += 1
    #pp.pprint(myD)

    k = 0
    xWingD = {}
    combSet = combinations(myD.values(), 2)
    for comb in combSet:
        #print(comb)
        if comb[0]['C_val'] == comb[1]['C_val'] and comb[0]['B_cols'] == comb[1]['B_cols']:

            xWingD[k] = { 'A_rows': [ comb[0]['A_row'], comb[1]['A_row'] ],
                          'B_cols':   comb[0]['B_cols'],
                          'C_val' :   comb[0]['C_val']  }
            k += 1
    if lclPrintDic['xwPrn'] >= 1:
        for k,v in xWingD.items():
            myDstr = pp.pformat(v)
            print('\n    {} {}'.format(house, myDstr), end = '')
        print()

    alreadyPrinted = False
    for xWing in xWingD.values():
        for rIdx,row in enumerate(xCanidates):
            for cIdx in xWing['B_cols']:
                if (rIdx not in xWing['A_rows'])  and \
                    (row[cIdx] != 0) and \
                    (xWing['C_val'] in row[cIdx]):
                    xCanidates[rIdx][cIdx].remove(xWing['C_val'])
                    numPruned += 1

                    if lclPrintDic['xwPrn'] >= 2:
                        pr.printCanidates(xCanidates, alreadyPrn = alreadyPrinted)
                        #print({True: '', False: '   {}'.format(xWing)} [alreadyPrinted])
                        alreadyPrinted = True

                    if lclPrintDic['xwPrn'] >= 1:
                        print('      remove {} from ({},{})'.format(xWing['C_val'], rIdx, cIdx))

    cpyDic = {'row':copy.deepcopy, 'col':mp.mapRowsToCols, 'sqr':mp.mapRowsToSqrs}
    canidates = cpyDic[house](xCanidates)

    return(numPruned, canidates)
############################################################################

# map sqrs to rows -> xCanidates
#
# find all nums in rows of xCanidates (sqrs of canidates) that appear exactly twice
#
# if the nums that appear exactly twice are in cols of xCanidates (sqrs of canidates)
# 0,1,2 or 3,4,5 of 6,7,8 then they are in the same row of canidates
# and hence are a 'row' pointing pair.
#
# if the nums that appear exactly twice are in cols of xCanidates (sqrs of canidates)
# 0,3,6 or 1,4,7 of 2,5,8 then they are in the same col of canidates
# and hence are a 'col' pointing pair.
#
# process the pointing pairs in canidates.

def prunePointingPairs(canidates, house, lclPrintDic):
    xCanidates = mp.mapSrqsToRows(canidates)
    numPruned  = 0

    # find all nums in rows of xCanidates (sqrs of canidates) that appear exactly twice
    allBinsHeightTwo = []
    for row in xCanidates:
        flatRow = flatten(row)
        histRow = genHistogram(flatRow)
        allBinsHeightTwo.append([ x[0] for x in histRow if x[1] == 2 and x[0] != 0])
    ####################################################################################

    # Place above data in a dict and add to data the two offset within the square
    # where the two nums appear. Note that pair may not be on the same row/col ...
    k = 0
    allBinsHeightTwoD = {}
    for idx,lstOfVals in enumerate(allBinsHeightTwo):
        for val in lstOfVals:
            cols = [ c for c,lst in enumerate(xCanidates[idx]) if lst != 0 and val in lst ]
            allBinsHeightTwoD[k] = { 'A_sqr':idx, 'B_idxs':cols, 'C_val':val,  }
            k += 1
    ####################################################################################

    # Create a new dict (either row or col, but not both) that are a subset of above dict.
    # New dict only contains the elements of the old dict that have the pair (in the square)
    # on the same row/col.  One of the two dicts will be empty.
    k = 0
    ppRowRqmt = [[0,1,2],[3,4,5],[6,7,8]]
    ppColRqmt = [[0,3,6],[1,4,7],[2,5,8]]
    ppRowD = {}
    ppColD = {}
    if house == 'row': rqmt = ppRowRqmt
    if house == 'col': rqmt = ppColRqmt
    for val in allBinsHeightTwoD.values():
        for el in rqmt:
            if all(x in el for x in val['B_idxs']):
                if house == 'row': ppRowD[k] = val
                if house == 'col': ppColD[k] = val
                k += 1
    ####################################################################################

    # create a 3rd dict (either row or col, but not both) that is the same as the above
    # dict except sqr,offset mapped to abs r,c.
    k = 0
    ppRowAbsCoordD = {}
    ppColAbsCoordD = {}
    if house == 'row': ppD = ppRowD
    if house == 'col': ppD = ppColD
    for val in ppD.values():
        row0,col0= mp.getRowColFromSqrOffset(val['A_sqr'],val['B_idxs'][0])
        row1,col1= mp.getRowColFromSqrOffset(val['A_sqr'],val['B_idxs'][1])
        if house == 'row': ppRowAbsCoordD[k]= {'aRow':row0,'bCols':[col0,col1],'cVal':val['C_val']}
        if house == 'col': ppColAbsCoordD[k]= {'aCol':col0,'bRows':[row0,row1],'cVal':val['C_val']}
        k += 1
    ####################################################################################

    # debug prints
    if lclPrintDic['ppPrn'] >= 3:
        thingsPprint = { #'allBinsHeightTwo':allBinsHeightTwo,
                         'allBinsHeightTwoD':allBinsHeightTwoD,
                         'ppRowD':ppRowD,
                         'ppColD':ppColD,
                         'ppRowAbsCoordD':ppRowAbsCoordD,
                         'ppColAbsCoordD':ppColAbsCoordD 
                         }

        for k,v in thingsPprint.items():
            myStr = ''
            print('     {} ({})'.format(k, house))
            for ii in range(len(v)):
                myStr = pp.pformat(v[ii])
                print('    ',myStr)
            print()

    ####################################################################################

    # perform associated removals Note only one of the 2 dicts looped through below will
    # have anything in it.
    alreadyPrinted = False
    rowsProcessed = []
    for val in ppRowAbsCoordD.values():
        if val['aRow'] not in rowsProcessed:
            if lclPrintDic['ppPrn'] >= 1: print( f'     Processing {val}')
            cols = [ x for x in range(9) if x not in val['bCols'] ]
            for cIdx in cols:
                if canidates[val['aRow']][cIdx]!=0 and val['cVal'] in canidates[val['aRow']][cIdx]:

                    if lclPrintDic['ppPrn'] >= 2:
                        pr.printCanidates(canidates, alreadyPrn = alreadyPrinted)
                        alreadyPrinted = True

                    canidates[val['aRow']][cIdx].remove(val['cVal'])
                    numPruned += 1

                    if lclPrintDic['ppPrn'] >= 1:
                        print('       remove {} from ({},{})'.format(val['cVal'],val['aRow'],cIdx))

    alreadyPrinted = False
    colsProcessed = []
    for val in ppColAbsCoordD.values():
        if val['aCol'] not in colsProcessed:
            if lclPrintDic['ppPrn'] >= 1: print( f'     Processing {val}')
            rows = [ x for x in range(9) if x not in val['bRows'] ]
            for rIdx in rows:
                if canidates[rIdx][val['aCol']]!=0 and val['cVal'] in canidates[rIdx][val['aCol']]:

                    if lclPrintDic['ppPrn'] >= 2:
                        pr.printCanidates(canidates, alreadyPrn = alreadyPrinted)
                        alreadyPrinted = True

                    canidates[rIdx][val['aCol']].remove(val['cVal'])
                    numPruned += 1

                    if lclPrintDic['ppPrn'] >= 1:
                        print('       remove {} from ({},{})'.format(val['cVal'],rIdx,val['aCol']))
    ####################################################################################

    return numPruned,canidates
############################################################################

def prYWingDict(v):
    print('    cord   = {}'.format(v[ 'cord'   ]))
    print('    sqrs   = {}'.format(v[ 'sqrs'   ]))
    print('    vals   = {}'.format(v[ 'vals'   ]))
    print()

    print('    pIdx   = {}'.format(v[ 'pIdx'   ]))
    print('    Z      = {}'.format(v[ 'Z'      ]))
    print('    rmvIdx = {}'.format(v[ 'rmvIdx' ]))

    #print('    rSee   = {}'.format(v['rSee'][0]))
    #print('             {}'.format(v['rSee'][1]))
    #print('             {}'.format(v['rSee'][2]))

    #print('    cSee   = {}'.format(v['cSee'][0]))
    #print('             {}'.format(v['cSee'][1]))
    #print('             {}'.format(v['cSee'][2]))

    #print('    sSee   = {}'.format(v['sSee'][0]))
    #print('             {}'.format(v['sSee'][1]))
    #print('             {}'.format(v['sSee'][2]))

    #print('    aSee   = {}'.format(v['allSeeSet'][0]))
    #print('             {}'.format(v['allSeeSet'][1]))
    #print('             {}'.format(v['allSeeSet'][2]))
    print()
    return 0
#############################################################################
                                     #
def pruneyWings (lclCanidates, lclPrintDic):
    numPruned = 0
    coordsOfAllPairs  = [ [r,c] for r in range(9) for c in range(9) \
        if lclCanidates[r][c] != 0 and len(lclCanidates[r][c]) == 2]
    combSet3pairsCord = combinations(coordsOfAllPairs, 3)
    combLst3pairsCord = list(combSet3pairsCord)

    yWingDict = {}
    for ii,comb in enumerate(combLst3pairsCord):

        vals,rSee,cSee,sSee,aSet,sqrs = [],[],[],[],[],[]
        for cord in comb:
            rowsInSq, colsInSq = mp.findRowsColsInSquare(cord[0], cord[1])

            sqr = cord[0]//3*3 + cord[1]//3
            v   = lclCanidates[cord[0]][cord[1]]
            r   = [ [cord[0],c] for c in range(9) ]
            c   = [ [r,cord[1]] for r in range(9) ]
            s   = [ [r,c] for r in rowsInSq for c in colsInSq]
            a   = [ x for x in r + c + s if x!= [cord[0], cord[1]] ] # self not in lst.
            aS  = set( tuple(x) for x in a ) # no self, no dups.
            sqrs.append(sqr)
            vals.append(v)
            rSee.append(r)
            cSee.append(c)
            sSee.append(s)
            aSet.append(aS)

        noValDups = list(map(list, set(map(tuple, map(set, vals)))))
        histFlat  = genHistogram(flatten(vals))

        # Do the 3 cells look like [a,b] [a,z] [b,z]? Yes, potential Y-Wing.
        if len(noValDups) == 3 and len(histFlat) == 3:

            yWingDict[ii] = {'cord':   list(comb), 'sqrs': sqrs,
                             'pIdx':   None,
                             'Z':      None,
                             'rmvIdx': None,
                             'vals':   vals,
                             'rSee':   rSee, 'cSee': cSee, 'sSee': sSee,
                             'allSeeSet': aSet}

    # Wings must     be in the same r or c or s as the pivot.
    # Wings must not be in the same r or c or s as each other.
    yWingDict2 = {}
    for k,v in yWingDict.items():
        aSeesB = v['cord'][0][0] == v['cord'][1][0] or \
                 v['cord'][0][1] == v['cord'][1][1] or \
                 v['sqrs'][0]    == v['sqrs'][1]

        aSeesC = v['cord'][0][0] == v['cord'][2][0] or \
                 v['cord'][0][1] == v['cord'][2][1] or \
                 v['sqrs'][0]    == v['sqrs'][2]

        bSeesC = v['cord'][1][0] == v['cord'][2][0] or \
                 v['cord'][1][1] == v['cord'][2][1] or \
                 v['sqrs'][1]    == v['sqrs'][2]

        seesLst = [aSeesB, aSeesC, bSeesC]
        if seesLst.count(False) == 1: # This is one!
            pIdx = 2- seesLst.index(False)
            notP = [i for i in range(3) if i != pIdx]
            Z    = [ x for x in v['vals'][notP[0]] if x not in v['vals'][pIdx] ][0]

            delCrds = set.intersection( v['allSeeSet'][notP[0]], v['allSeeSet'][notP[1]] )
            rmvIdx  = [ x for x in delCrds if x!= (v['cord'][pIdx][0], v['cord'][pIdx][1]) ]

            yWingDict2[k]           = v
            yWingDict2[k]['pIdx']   = pIdx    # pivot.
            yWingDict2[k]['Z']      = Z       # Val to del.
            yWingDict2[k]['rmvIdx'] = rmvIdx  # Where to del from.

    alreadyPrinted = False
    for k,v in yWingDict2.items():
        if lclPrintDic['ywPrn'] >= 1:
            print('\n  Processing key {}'.format(k))
            prYWingDict(v)
        for cord in v['rmvIdx']:
            if lclCanidates[cord[0]][cord[1]]!=0 and v['Z'] in lclCanidates[cord[0]][cord[1]]:

                if lclPrintDic['ywPrn'] >= 2:
                    pr.printCanidates(lclCanidates, alreadyPrn = alreadyPrinted)
                    alreadyPrinted = True

                lclCanidates[cord[0]][cord[1]].remove(v['Z'])
                numPruned += 1

                if lclPrintDic['ywPrn'] >= 1:
                    print('     remove {} from ({},{})'.format(v['Z'], cord[0],cord[1]))

    return numPruned,lclCanidates
#############################################################################
