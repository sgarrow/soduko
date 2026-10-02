from itertools import combinations
import sys
import time
import copy
import pprint        as pp

import printRoutines as pr
import utils         as ut
import fillRoutines  as fr
import ana           as an
import cfg

import prune.nakedHiddenTups as nht
import prune.xWing           as xw
import prune.yWing           as yw
import prune.pointingPair    as pnp
import prune.claimCanidates  as cc

VER = 'v2.6.5 - 01-Oct-2026'
#############################################################################

def updateCanidatesList(lclSolution,lclCanidates):
    print('\nUpdating Canidates list')
    cols=[[row[i] for row in lclSolution] for i in range(len(lclSolution[0]))]

    for rIdx,row in enumerate(lclSolution):
        for cIdx,elem in enumerate(row):
            col = cols[cIdx]

            if elem != 0:
                lclCanidates[rIdx][cIdx] = 0
                continue
            for num in [1,2,3,4,5,6,7,8,9]:

                inSquare = False
                rowsInSquare,colsInSquare= ut.findRowsColsInSquare(rIdx,cIdx)

                for ris in rowsInSquare:
                    for cis in colsInSquare:
                        if lclSolution[ris][cis] == num:
                            inSquare = True
                            break
                    if inSquare:
                        break

                if( row.count(num)==0 and col.count(num)==0 and not inSquare):
                    if lclCanidates[rIdx][cIdx] != 0:
                        lclCanidates[rIdx][cIdx].append(num)
    totSum = 0
    for rIdx,row in enumerate(lclCanidates):
        for cIdx,elem in enumerate(row):
            if lclCanidates[rIdx][cIdx] != 0:
                totSum += sum(lclCanidates[rIdx][cIdx])

    print(62*'*')
    return lclCanidates
#############################################################################

def pruneNht(lclCanidates, cfgDic):

    hiddenNakedLst = [ 'hidden', 'naked' ]
    houseLst       = [ 'row','col','sqr' ]
    tupSizeLst     = [4,3,2]

    #hiddenNakedLst = [ 'hidden']
    #hiddenNakedLst = [ 'naked']
    #houseLst       = [ 'row','col' ]
    #houseLst       = [ 'row' ]
    #tupSizeLst     = [2,3]
    #tupSizeLst     = [2]

    totNumPruned   = 0
    for hideNkd in hiddenNakedLst:
        for tupSize in tupSizeLst:
            for house in houseLst:

                numPruned, lclCanidates = nht.pruneNakedAndHiddenTuples(
                lclCanidates, house, hideNkd,tupSize, cfgDic)

                totNumPruned += numPruned

                if cfgDic['nh']['prnLevel'] >= 1:
                    print('    Pruning {:6} {}-tuples in {}s. '.\
                        format(hideNkd,tupSize,house), end = '')
                    print('Prunned: {:3}'.format(numPruned))

    return totNumPruned, lclCanidates
#############################################################################

def prunePp(lclCanidates, cfgDic):

    houseLst   = [ 'row','col' ]
    tupSizeLst = [2,3]

    #houseLst = [ 'row']
    #tupSizeLst = [2]

    totNumPruned = 0
    for tupSize in tupSizeLst:
        for house in houseLst:

            numPruned, lclCanidates = \
            pnp.prunePointingPairs( lclCanidates, house, tupSize, cfgDic)

            totNumPruned += numPruned
    
            if cfgDic['pp']['prnLevel'] >= 1:
                print('    Pruning Pointing {}s in {}s. '.\
                    format(tupSize,house), end = '')
                print('Prunned: {:3}'.format(numPruned))

    return totNumPruned, lclCanidates
#############################################################################

def pruneXw(lclCanidates, cfgDic):

    houseLst = [ 'row','col' ]

    #houseLst = [ 'row' ]

    totNumPruned = 0
    for house in houseLst:
        numPruned,lclCanidates=xw.pruneXwings(lclCanidates,house,cfgDic)
        totNumPruned += numPruned

        if cfgDic['xw']['prnLevel'] >= 1:
            print('    Pruning xWings in {}s. '.format(house), end = '')
            print('Prunned: {:3}'.format(numPruned))

    return totNumPruned, lclCanidates
#############################################################################

def pruneYw(lclCanidates, cfgDic):

    totNumPruned = 0
    numPruned, lclCanidates = yw.pruneyWings(lclCanidates, cfgDic)
    totNumPruned += numPruned

    if cfgDic['xw']['prnLevel'] >= 1:
        print('    Pruning yWings. ', end = '')
        print('Prunned: {:3}'.format(numPruned))

    return totNumPruned, lclCanidates
#############################################################################

def pruneCc(lclCanidates, cfgDic):

    houseLst = [ 'row','col' ]
    #houseLst = [ 'row' ]

    totNumPruned = 0

    for house in houseLst:
        numPruned, lclCanidates = cc.pruneClaimCanidates(lclCanidates, house, cfgDic)
        totNumPruned += numPruned

        if cfgDic['cc']['prnLevel'] >= 1:
            print('    Pruning Claiming Canidates in {}s. '.format(house), end = '')
            print('Prunned: {:3}'.format(numPruned))

    return totNumPruned, lclCanidates
#############################################################################

#if 'ss' in clArgs: input('Return to continue')
def pruneCanidates(lclCanidates,lclPruneSet,lclPruneDicOfFuncs,cfgDic):
    if len(lclPruneSet) == 0:
        return lclPruneDicOfFuncs, lclCanidates

    print('\nPruning canidates list')
    cumStr = ''

    # Keep prunning until all prune functions return 0 prunes done.
    prunedAtLeastOne = True
    while prunedAtLeastOne:

        # Loop over all (enabled) prune functions.
        prunedAtLeastOne = False
        for theKey,v in lclPruneDicOfFuncs.items():
            if v['func'] is pruneNht and not 'nh' in lclPruneSet: continue
            if v['func'] is prunePp  and not 'pp' in lclPruneSet: continue
            if v['func'] is pruneXw  and not 'xw' in lclPruneSet: continue
            if v['func'] is pruneYw  and not 'yw' in lclPruneSet: continue
            if v['func'] is pruneCc  and not 'cc' in lclPruneSet: continue

            printLevel = 0
            if   v['func'] is pruneNht: 
               printLevel = cfgDic['nh']['prnLevel']
            elif v['func'] is prunePp:
               printLevel = cfgDic['pp']['prnLevel']
            elif v['func'] is pruneXw:
               printLevel = cfgDic['xw']['prnLevel']
            elif v['func'] is pruneYw:
               printLevel = cfgDic['yw']['prnLevel']
            elif v['func'] is pruneCc:
               printLevel = cfgDic['cc']['prnLevel']

            passNum            = 0
            numPrunnedThisPass = 0
            numPrunnedThisLoop = []

            # Loop over this prune function until it returns 0 prunes done.
            while True:

                if printLevel >= 1:
                    print('  {:9} pass {}'.\
                        format(theKey, passNum, numPrunnedThisPass))

                numPrunnedThisPass, lclCanidates = v['func'](lclCanidates,
                                                             cfgDic)

                if printLevel >= 1:
                    print('  Prunned {:3}'.format(numPrunnedThisPass))

                numPrunnedThisLoop.append(numPrunnedThisPass)
                #cumStr+='{:9} prunned {}\n'.format(theKey,numPrunnedThisPass)
                passNum += 1

                if numPrunnedThisPass > 0:
                    prunedAtLeastOne = True
                else:
                    break

            v['numPrunned'].append(numPrunnedThisLoop)
            print('  Total Prunned by {:9} ({} passes) = {:3}'.\
                format( theKey, passNum, sum(v['numPrunned'][-1])))
            print(31*'*')

        print(31*'*')

    #print(cumStr)
    print(62*'*')

    return lclPruneDicOfFuncs, lclCanidates
#############################################################################

def fillSolution(lclSolution, lclCanidates, lclfillDicOfFuncs, cfgDic):
    totalNumFilled = 0

    print('\nFilling in solution cells')
    for theK in lclfillDicOfFuncs:

        numFilled, lclSolution = \
        lclfillDicOfFuncs[theK]['func']( lclSolution, lclCanidates,
                                         cfgDic, theK )

        totalNumFilled                     += numFilled
        lclfillDicOfFuncs[theK]['calls']   += 1
        lclfillDicOfFuncs[theK]['replace'] += numFilled

        if sum(x.count(0) for x in lclSolution)==0:
            break

    print(f'Total filled {totalNumFilled:2d}')
    print(62*'*')
    #if 'ss' in clArgs: input('Return to continue')

    return totalNumFilled, lclSolution, lclfillDicOfFuncs
#############################################################################

def initfillDicOfFuncsCntrs(lclfillDicOfFuncs):
    for theK in lclfillDicOfFuncs:
        lclfillDicOfFuncs[theK]['calls'  ] = 0
        lclfillDicOfFuncs[theK]['replace'] = 0
    return lclfillDicOfFuncs
#############################################################################

def checkStatus(sln):
    cpyDic={'row':copy.deepcopy,'col':ut.mapColsToRows,'sqr':ut.mapSrqsToRows}

    cumPassed = True
    for v in cpyDic.values():
        s = v(sln)
        for row in s:
            myCnt  = [ row.count(x) for x in row ]
            passed = not any( x != 1 for x  in myCnt)
            #print('house-{} idx-{} sts-{}'.format(k,rIdx,passed))
            if not passed:
                cumPassed = False
    return cumPassed
#############################################################################

def solvePuzzle(lclPuzzleDict, lclPruneSet, cfgDic):
    fillDicOfFuncs = {
    'one': { 'func': fr.fillViaOneCanidate, 'calls': 0, 'replace': 0 },
    'row': { 'func': fr.fillViaRCHistAnal,  'calls': 0, 'replace': 0 },
    'col': { 'func': fr.fillViaRCHistAnal,  'calls': 0, 'replace': 0 },
    'sqr': { 'func': fr.fillViaRCHistAnal,  'calls': 0, 'replace': 0 }}

    pruneDicOfFuncs = {
    'prune_XW' : { 'func': pruneXw,  'numPrunned': []},
    'prune_NHT': { 'func': pruneNht, 'numPrunned': []},
    'prune_PP' : { 'func': prunePp,  'numPrunned': []},
    'prune_YW' : { 'func': pruneYw,  'numPrunned': []},
    'prune_CC' : { 'func': pruneCc,  'numPrunned': []}}
    ###########################################################

    solution = [x[:] for x in lclPuzzleDict['puzzle'] ]
    lclPuzzleDict['start0s'] = sum(x.count(0) for x in solution)
    fillDicOfFuncs = initfillDicOfFuncsCntrs(fillDicOfFuncs)

    while True:
        numZerosBeforeAllFill = sum(x.count(0) for x in solution)
        if sum(x.count(0) for x in solution)==0:
            break
        numberFilled = 1
        while numberFilled:

            if sum(x.count(0) for x in solution)==0:
                break

            canidates = [[ [] for ii in range(9)] for jj in range(9)]
            canidates = updateCanidatesList(solution, canidates)

            pruneDicOfFuncs,canidates = \
            pruneCanidates(canidates,lclPruneSet,pruneDicOfFuncs,cfgDic)

            numberFilled, solution, fillDicOfFuncs = \
            fillSolution(solution,canidates,fillDicOfFuncs,cfgDic)

        numZerosAfterAllFill = sum(x.count(0) for x in solution)
        if  numZerosAfterAllFill in (numZerosBeforeAllFill,0):
            break
        numZerosBeforeAllFill = numZerosAfterAllFill
    # end while loop for this puzzle

    if numZerosAfterAllFill != 0:
        lclPuzzleDict['passed'] = False
    else:
        status = checkStatus(solution)
        lclPuzzleDict['passed'] = status


    lclPuzzleDict['end0s']    = numZerosAfterAllFill
    lclPuzzleDict['solution'] = solution
    lclPuzzleDict['prunes']   = lclPruneSet
    lclPuzzleDict['oC']       = fillDicOfFuncs['one']['calls'  ]
    lclPuzzleDict['oR']       = fillDicOfFuncs['one']['replace']
    lclPuzzleDict['rC']       = fillDicOfFuncs['row']['calls'  ]
    lclPuzzleDict['rR']       = fillDicOfFuncs['row']['replace']
    lclPuzzleDict['cC']       = fillDicOfFuncs['col']['calls'  ]
    lclPuzzleDict['cR']       = fillDicOfFuncs['col']['replace']
    lclPuzzleDict['sC']       = fillDicOfFuncs['sqr']['calls'  ]
    lclPuzzleDict['sR']       = fillDicOfFuncs['sqr']['replace']

    print(62*'#')
    #pp.pprint(canidates)
    return lclPuzzleDict
#############################################################################

def getGuesses(lclSolution):
    lclCanidates = [[ [] for ii in range(9)] for jj in range(9)]
    lclCanidates = updateCanidatesList(lclSolution, lclCanidates)

    lenCanRows = []
    for row in lclCanidates:
        lenCanRow = [ 0 if row[c] == 0 else len(row[c]) for c in range(0,9) ]
        lenCanRows.append(lenCanRow)

    lenCanRowsBySqr = []
    for row in lenCanRows:
        twoD = [row[ii:ii+3] for ii in range(0,len(row),3)]
        lenCanRowsBySqr.append(twoD)

    maxLenCanRowsBy3Cols = []
    for row in lenCanRowsBySqr:
        maxLenCanBySqr = [ max(el) for el in row ]
        maxLenCanRowsBy3Cols.append(maxLenCanBySqr)

    possibleIdxs = [ [0,1,2], [0,2,1], [1,0,2], [1,2,0], [2,0,1], [2,1,0]]
    tryLst = []
    for jj in range(3):
        tryL = []
        for idxLst in possibleIdxs:
            tLst = [ maxLenCanRowsBy3Cols[jj*3:(jj+1)*3][0][idxLst[0]],
                     maxLenCanRowsBy3Cols[jj*3:(jj+1)*3][1][idxLst[1]],
                     maxLenCanRowsBy3Cols[jj*3:(jj+1)*3][2][idxLst[2]]
                   ]
            tryL.append(tLst)
        tryLst.append(tryL)

    tryLstNo0 = []
    for el in tryLst:
        tryLstNo0.append([ x for x in el if 0 not in x ])

    numManuallyAdded = 0
    if tryLstNo0 == [[],[],[]]:
        print('manually adding')
        firstTryCoord = []
        canVals  = []
        for rIdx,row in enumerate(lclCanidates):
            for cIdx,possibleCanidate in enumerate(row):
                if possibleCanidate != 0:
                    firstTryCoord.append([rIdx,cIdx])
                    canVals.append(possibleCanidate)
                    numManuallyAdded += 1
                    if numManuallyAdded == 3:
                        break
            if numManuallyAdded == 3:
                break

        canValsLst = []
        for x in canVals[0]:
            for y in canVals[1]:
                for z in canVals[2]:
                    canValsLst.append([x,y,z])
    else:
        tryAbsCoord = []
        for jj,rowOfSqrsTLst in enumerate(tryLstNo0):
            for tryEl in rowOfSqrsTLst:
                c02 = [jj*3+0, lenCanRows[jj*3+0].index(tryEl[0])]
                c35 = [jj*3+1, lenCanRows[jj*3+1].index(tryEl[1])]
                c68 = [jj*3+2, lenCanRows[jj*3+2].index(tryEl[2])]
                tryAbsCoord.append([c02,c35,c68])

        tryAbsCoordUniqueSqrs = []
        for threeCoords in tryAbsCoord:
            s1 = threeCoords[0][1]//3
            s2 = threeCoords[1][1]//3
            s3 = threeCoords[2][1]//3
            sSet = set([s1,s2,s3])
            if len(sSet) == 3:
                tryAbsCoordUniqueSqrs.append(threeCoords)

        canVals  = []
        firstTryCoord = []
        if len(tryAbsCoordUniqueSqrs) > 0:
            firstTryCoord = tryAbsCoordUniqueSqrs[0]
            for coord in tryAbsCoordUniqueSqrs[0]:
                canVals.append([ x for x in lclCanidates[coord[0] ][coord[1]]])

        canValsLst = []
        for x in canVals[0]:
            for y in canVals[1]:
                for z in canVals[2]:
                    canValsLst.append([x,y,z])

    #print()
    #print('canidates')
    #pr.printCanidates(lclCanidates)
    #print()
    #print('length canidates - rows')
    #pp.pprint(lenCanRows)
    #print()
    #print('length canidates - sqrs')
    #pp.pprint(lenCanRowsBySqr)
    #print()
    #print('max length canidates rows by 3 cols')
    #pp.pprint(maxLenCanRowsBy3Cols)
    #print()
    #print('tryLst for 3 rows of squares')
    #pp.pprint(tryLst)
    #print()
    #print('tryLst No zeros for 3 rows of squares')
    #pp.pprint(tryLstNo0)
    #print()
    #
    #if numManuallyAdded == 0:
    #    print('tryAbsCoord')
    #    pp.pprint(tryAbsCoord)
    #    print()
    #    print('tryAbsCoordUnique Squares')
    #    for x in tryAbsCoordUniqueSqrs:
    #        print(x)
    #
    #print()
    #print('canVals')
    #pp.pprint(canVals)
    #print()
    #
    #print('firstTryCoord')
    #pp.pprint( firstTryCoord)
    #print()
    #print('canValsLst')
    #pp.pprint(canValsLst)
    #print()
    return firstTryCoord, canValsLst
#############################################################################

if __name__ == '__main__':
    from puzzles import puzzlesDict
    print(VER)
    cumAllStr = ''
    cumSumStr = ''
    ###########################################################

    error, rspStr, mnCfgDic = cfg.mkCfgDictPikleFile()

    pruneLst = [ k for k,v in mnCfgDic.items() \
                 if v['isPrundFunc'] == 1 and v['enabled'] == 1 ]
    allSets  = set()
    for ii in range(0,len(pruneLst)+1):
        allSets = set.union(allSets,set(combinations(pruneLst, ii)))

    #pp.pprint(mnCfgDic)
    #print('\n')
    #print('\npruneLst')
    #print(pruneLst)
    #print('\nallSets')
    #pp.pprint(allSets)
    ###########################################################

    if mnCfgDic[ 'analyze' ][ 'enabled' ] == 1 and \
       mnCfgDic[ 'guess'   ][ 'enabled' ] == 1:
        print('\n  ERROR. Can\'t analyze and guesss together.\n')
        sys.exit()

    if mnCfgDic[ 'analyze' ][ 'enabled' ] == 1: 
        pruneSets = allSets
    else: 
        pruneSets = [pruneLst]
    pp.pprint(pruneSets)
    ###########################################################

    puzDicKeys = list(puzzlesDict.keys())
    print()
    for ii,k in enumerate(puzDicKeys):
        print('  {:2} - {}'.format( ii,k ))
    print( '   a - all')
    print( '   q - quit')
    puzIdxs = input('\n Choice -> ' ).split()

    if 'q' in puzIdxs:
        sys.exit()

    if 'a' in puzIdxs:
        puzIdxs = [ii for ii,k in enumerate(puzDicKeys)]
    dsrdKeys = [puzDicKeys[int(x)] for x in puzIdxs]
    ###########################################################

    startTime = time.time()
    for pNme,pIdx in zip(dsrdKeys,puzIdxs):
        print(' ### Start {} ###'.format(pNme))
        pDat = puzzlesDict[pNme]
        for pruneSet in pruneSets:
            puzzlesDict[pNme] = solvePuzzle(pDat, pruneSet, mnCfgDic)
            aStr, sStr = pr.printResults(pNme, pIdx, pDat)
            cumAllStr += aStr
            cumSumStr += sStr

            if not puzzlesDict[pNme]['passed'] and mnCfgDic['guess']['enabled'] == 1:
                print('{} guessing'.format(pNme))
                #input()
                tryCords, tryVals = \
                getGuesses(puzzlesDict[pNme]['solution'])

                for tVals in tryVals:
                    puzzlesDict[pNme]['guesses'] += 1
                    for ii,k in enumerate(tryCords):
                        puzzlesDict[pNme]['puzzle'][k[0]][k[1]] = tVals[ii]

                    puzzlesDict[pNme] = solvePuzzle(pDat, pruneSet, mnCfgDic)
                    aStr, sStr = pr.printResults(pNme, pIdx, pDat)
                    cumAllStr += aStr
                    cumSumStr += sStr
                    if puzzlesDict[pNme]['passed']:
                        break

                for ii,k in enumerate(tryCords):
                    puzzlesDict[pNme]['puzzle'][k[0]][k[1]] = 0

        print(' ### End   {} ###'.format(pNme))
    print(cumAllStr)
    print(cumSumStr)

    for k in puzzlesDict.keys():
        if puzzlesDict[k]['guesses'] > 0:
            print(' Made {:3} guesses on puzzle {}'.format(puzzlesDict[k]['guesses'],k))

    if mnCfgDic['analyze']['enabled'] == 1:
        with open('pData.txt', 'w', encoding='utf-8') as pFile:
            pFile.write(cumSumStr)
        an.analyze()

    endTime = time.time()
    print('\n Execution time = {:7.2f} seconds.'.format(endTime-startTime))
