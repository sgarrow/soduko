from itertools import combinations
import utils         as ut
import printRoutines as pr
############################################################################

def pruneyWings (lclCanidates, lclPrintDic):
    numPruned = 0
    coordsOfAllPairs  = [ [r,c] for r in range(9) for c in range(9) \
        if lclCanidates[r][c] != 0 and len(lclCanidates[r][c]) == 2]
    combSet3pairsCord = combinations(coordsOfAllPairs, 3)
    combLst3pairsCord = list(combSet3pairsCord)

    #print( '  coordinates of all cells with only two canidates:' )
    #[ print(c,' =',lclCanidates[c[0]][c[1]]) for c in coordsOfAllPairs ]
    #print( '  all combinations of above coordinates:' )
    #[ print(c) for c in combLst3pairsCord ]
    #input()

    yWingDict = {}
    for ii,comb in enumerate(combLst3pairsCord):

        vals,rSee,cSee,sSee,aSet,sqrs = [],[],[],[],[],[]
        for cord in comb:
            rowsInSq, colsInSq = ut.findRowsColsInSquare(cord[0], cord[1])

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
        histFlat  = ut.genHistogram(ut.flatten(vals))

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
            z    = [ x for x in v['vals'][notP[0]] if x not in v['vals'][pIdx] ][0]

            delCrds = set.intersection( v['allSeeSet'][notP[0]], v['allSeeSet'][notP[1]] )
            rmvIdx  = [ x for x in delCrds if x!= (v['cord'][pIdx][0], v['cord'][pIdx][1]) ]

            yWingDict2[k]           = v
            yWingDict2[k]['pIdx']   = pIdx    # pivot.
            yWingDict2[k]['Z']      = z       # Val to del.
            yWingDict2[k]['rmvIdx'] = rmvIdx  # Where to del from.

    alreadyPrinted = False
    for k,v in yWingDict2.items():
        if lclPrintDic['ywPrn'] >= 1:
            print('\n  Processing key {}'.format(k))
            pr.prYWingDict(v)
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
