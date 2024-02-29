#  C:\Users\bendr\AppData\Roaming\Python\Python311\Scripts\pylint.exe  .\soduko.py

import pprint        as pp
import sys
import time
import copy
from itertools import combinations
import printRoutines as pr
import mapping       as mp
import fillRoutines  as fr
import pruneRoutines as rr
import ana           as an
import fillRoutines  as fr

NEWLINE = '\n'
STARS44 = 44*'*'
POUND62 = 62*'#'
#############################################################################

def updateCanidatesList(lclSolution,lclCanidates):
    print('\nUpdating Canidates list')
    cols = [ [ row[i] for row in lclSolution] for i in range(len(lclSolution[0]))]

    for rIdx,row in enumerate(lclSolution):
        for cIdx,elem in enumerate(row):
            col = cols[cIdx]

            if elem != 0:
                lclCanidates[rIdx][cIdx] = 0
                continue
            for num in [1,2,3,4,5,6,7,8,9]:

                inSquare = False
                rowsInSquare, colsInSquare = mp.findRowsColsInSquare(rIdx, cIdx)

                for ris in rowsInSquare:
                    for cis in colsInSquare:
                        if lclSolution[ris][cis] == num:
                            inSquare = True
                            break
                    if inSquare:
                        break

                #print('   inSquare={}'.format(inSquare))
                if( row.count(num) == 0 and col.count(num) == 0 and not inSquare):
                    #print('   Adding {} as canidate for {},{}'.format(ii,rIdx,cIdx))
                    if lclCanidates[rIdx][cIdx] != 0:
                        lclCanidates[rIdx][cIdx].append(num)
    totSum = 0
    for rIdx,row in enumerate(lclCanidates):
        for cIdx,elem in enumerate(row):
            if lclCanidates[rIdx][cIdx] != 0:
                totSum += sum(lclCanidates[rIdx][cIdx])
    #print('totSum = ', totSum)
    return lclCanidates
#############################################################################

def pruneNht(lclCanidates, clArgs):

    hiddenNakedLst = [ 'hidden', 'naked' ]
    #hiddenNakedLst = [ 'hidden']

    houseLst       = [ 'row','col','sqr' ]
    #houseLst       = [ 'row' ]

    tupSizeLst     = [4,3,2]
    #tupSizeLst     = [3]

    totNumPruned   = 0

    for hideNkd in hiddenNakedLst:
        for tupSize in tupSizeLst:
            for house in houseLst:
                #print('Pruning {:6} {}-tuples in {}s'.format(hn,N,h))
                numPruned, lclCanidates = \
                rr.pruneNakedAndHiddenTuples(lclCanidates, house, hideNkd, tupSize, clArgs)
                totNumPruned += numPruned

                if numPruned:
                    print(f'    Prunned {numPruned:2} RE: {hideNkd:6} {tupSize}-tuples in {house}s')

    return totNumPruned, lclCanidates
#############################################################################

def pruneXw(lclCanidates, clArgs):
    totNumPruned = 0
    houseLst = [ 'row','col' ]
    for house in houseLst:
        numPruned, lclCanidates = rr.pruneXwings(lclCanidates, house, clArgs)
        totNumPruned += numPruned

        if numPruned:
            print(f'    Prunned {numPruned:2} lclCanidates RE: X-Wings in {house}s')

    return totNumPruned, lclCanidates
#############################################################################

def pruneYw(lclCanidates, clArgs):
    totNumPruned = 0
    numPruned, lclCanidates = rr.pruneyWings(lclCanidates, clArgs)
    totNumPruned += numPruned

    if numPruned:
        print(f'    Prunned {numPruned:2} lclCanidates RE: Y-Wings.')

    return totNumPruned, lclCanidates
#############################################################################

def prunePp(lclCanidates, clArgs):
    totNumPruned = 0
    houseLst = [ 'row','col' ]
    #houseLst = [ 'row']
    for house in houseLst:
        numPruned, lclCanidates = rr.prunePointingPairs(lclCanidates, house, clArgs)
        totNumPruned += numPruned

        if numPruned:
            print(f'    Prunned {numPruned:2} lclCanidates RE: Pointing Pairs in {house}')

    return totNumPruned, lclCanidates
#############################################################################

def pruneCanidates(clArgs, lclPruneDicOfFuncs, lclCanidates):
    if len(clArgs) == 0:
        return lclPruneDicOfFuncs, lclCanidates

    print('\nPruning canidates list')

    prunedAtLeastOne   = True
    cumStr = ''
    while prunedAtLeastOne:                      # Loop over function group.

        prunedAtLeastOne   = False

        for theKey,v in lclPruneDicOfFuncs.items():   # Loop over each function.

            if v['func'] is pruneXw  and not 'xwOn' in clArgs: continue
            if v['func'] is pruneNht and not 'nhOn' in clArgs: continue
            if v['func'] is prunePp  and not 'ppOn' in clArgs: continue
            if v['func'] is pruneYw  and not 'ywOn' in clArgs: continue

            passNum            = 0
            numPrunnedThisPass = 0
            numPrunnedThisLoop = []

            while True:                          # Loop over one function.

                print('  {:9} pass {}'.format(theKey, passNum))
                numPrunnedThisPass, lclCanidates = v['func'](lclCanidates, clArgs)
                numPrunnedThisLoop.append(numPrunnedThisPass)
                if numPrunnedThisPass != 0:
                    cumStr += (f'  {theKey:9} prunned {numPrunnedThisPass}{NEWLINE}')
                passNum += 1

                if 'ss' in clArgs: input('Return to continue')

                if numPrunnedThisPass > 0:
                    prunedAtLeastOne = True
                else:
                    break

            v['numPrunned'].append(numPrunnedThisLoop)
            print('  Total Prunned {:9} {}'.format(theKey, sum(v['numPrunned'][-1])))
            print(31*'*')

        print(31*'*')

    print(cumStr)
    print(62*'*')

    return lclPruneDicOfFuncs, lclCanidates
#############################################################################

def fillSolution(lclSolution, lclCanidates, lclfillDicOfFuncs, clArgs ):
    totalNumFilled = 0

    print('\nFilling in solution cells')
    for theK in lclfillDicOfFuncs:
        numFilled, lclSolution = lclfillDicOfFuncs[theK]['func'](lclSolution,lclCanidates)
        totalNumFilled  += numFilled
        lclfillDicOfFuncs[theK]['calls']   += 1
        lclfillDicOfFuncs[theK]['replace'] += numFilled
    print(f'{NEWLINE}  Total filled {totalNumFilled:2d} {STARS44}')
    print(62*'*')
    if 'ss' in clArgs: input('Return to continue')

    return totalNumFilled, lclSolution, lclfillDicOfFuncs
#############################################################################

def initfillDicOfFuncsCntrs(lclfillDicOfFuncs):
    for theK in lclfillDicOfFuncs:
        lclfillDicOfFuncs[theK]['calls'  ] = 0
        lclfillDicOfFuncs[theK]['replace'] = 0
    return lclfillDicOfFuncs
#############################################################################

def checkStatus(sln):
    cpyDic = {'row':copy.deepcopy, 'col':mp.mapColsToRows, 'sqr':mp.mapSrqsToRows}

    cumPassed = True
    for k,v in cpyDic.items():
        s = v(sln)
        #pp.pprint(s)
        for rIdx,row in enumerate(s):
            myCnt  = [ row.count(x) for x in row ]
            passed = not(any( x != 1 for x  in myCnt))
            #print('house-{} idx-{} sts-{}'.format(k,rIdx,passed))
            if not passed:
                cumPassed = False
        #input()
    return cumPassed
#############################################################################

def solvePuzzle(aPuzzleDict, lclCmdLineArgs):

    fillDicOfFuncs = {
    'one': { 'func': fr.fillViaOneCanidate, 'calls': 0, 'replace': 0 },
    'row': { 'func': fr.fillViaRowHistAnal, 'calls': 0, 'replace': 0 },
    'col': { 'func': fr.fillViaColHistAnal, 'calls': 0, 'replace': 0 },
    'sqr': { 'func': fr.fillViaSqrHistAnal, 'calls': 0, 'replace': 0 }}

    pruneDicOfFuncs = {
    'prune_XW' : { 'func': pruneXw,  'numPrunned': []},
    'prune_NHT': { 'func': pruneNht, 'numPrunned': []},
    'prune_PP' : { 'func': prunePp,  'numPrunned': []},
    'prune_YW' : { 'func': pruneYw,  'numPrunned': []}}
    ###########################################################

    solution = [x[:] for x in aPuzzleDict['puzzle'] ]
    aPuzzleDict['start0s'] = sum(x.count(0) for x in solution)
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
                pruneCanidates(lclCmdLineArgs, pruneDicOfFuncs, canidates)
            numberFilled, solution, fillDicOfFuncs = \
                fillSolution(solution, canidates, fillDicOfFuncs, lclCmdLineArgs)

        numZerosAfterAllFill = sum(x.count(0) for x in solution)
        if  numZerosAfterAllFill in (numZerosBeforeAllFill,0):
            break
        numZerosBeforeAllFill = numZerosAfterAllFill
    # end while loop for this puzzle

    if numZerosAfterAllFill != 0:
        aPuzzleDict['passed'] = False
    else:
        status = checkStatus(solution)
        aPuzzleDict['passed'] = status


    aPuzzleDict['end0s']    = numZerosAfterAllFill
    aPuzzleDict['solution'] = solution
    aPuzzleDict['prunes']   = lclCmdLineArgs
    aPuzzleDict['oC']       = fillDicOfFuncs['one']['calls'  ]
    aPuzzleDict['oR']       = fillDicOfFuncs['one']['replace']
    aPuzzleDict['rC']       = fillDicOfFuncs['row']['calls'  ]
    aPuzzleDict['rR']       = fillDicOfFuncs['row']['replace']
    aPuzzleDict['cC']       = fillDicOfFuncs['col']['calls'  ]
    aPuzzleDict['cR']       = fillDicOfFuncs['col']['replace']
    aPuzzleDict['sC']       = fillDicOfFuncs['sqr']['calls'  ]
    aPuzzleDict['sR']       = fillDicOfFuncs['sqr']['replace']

    print(f'{POUND62}')
    return aPuzzleDict
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
    for ii in range(3):
        tryL = []
        for idxLst in possibleIdxs:
            tLst = [ maxLenCanRowsBy3Cols[ii*3:(ii+1)*3][0][idxLst[0]], 
                     maxLenCanRowsBy3Cols[ii*3:(ii+1)*3][1][idxLst[1]],
                     maxLenCanRowsBy3Cols[ii*3:(ii+1)*3][2][idxLst[2]] 
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
        for ii,rowOfSqrsTLst in enumerate(tryLstNo0):
            for TryEl in rowOfSqrsTLst:
                c02 = [ii*3+0, lenCanRows[ii*3+0].index(TryEl[0])]
                c35 = [ii*3+1, lenCanRows[ii*3+1].index(TryEl[1])]
                c68 = [ii*3+2, lenCanRows[ii*3+2].index(TryEl[2])]
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
    #pp.pprint(firstTryCoord)
    #print()
    #print('canValsLst')
    #pp.pprint(canValsLst)
    #print()
    #
    #exit()
    return firstTryCoord, canValsLst
#############################################################################



if __name__ == '__main__':
    from puzzles import puzzlesDict

    startTime = time.time()
    ###########################################################

    with open('cfgFile.txt', encoding='utf-8') as cfgFile:
        rawOptions = cfgFile.readlines()
    options = [ x.split() for x in rawOptions ]

    pruneLst = ['nhOn','xwOn','ppOn','ywOn']
    for option in options:
        if len(option) == 2:
            if option[0] == 'nhOn'  : nhOn   = int(option[1])
            if option[0] == 'xwOn'  : xwOn   = int(option[1]) 
            if option[0] == 'ppOn'  : ppOn   = int(option[1]) 
            if option[0] == 'ywOn'  : ywOn   = int(option[1]) 
                                      
            if option[0] == 'nhtPrn': nhtPrn = int(option[1]) 
            if option[0] == 'xwPrn' : xwPrn  = int(option[1]) 
            if option[0] == 'ppPrn' : ppPrn  = int(option[1]) 
            if option[0] == 'ywPrn' : ywPrn  = int(option[1]) 
            if option[0] == 'ss'    : ss     = int(option[1]) 

    if not nhOn: pruneLst.remove('nhOn')
    if not xwOn: pruneLst.remove('xwOn')
    if not ppOn: pruneLst.remove('ppOn')
    if not ywOn: pruneLst.remove('ywOn')

    pruneSet0 = set(combinations(pruneLst, 0))
    pruneSet1 = set(combinations(pruneLst, 1))
    pruneSet2 = set(combinations(pruneLst, 2))
    pruneSet3 = set(combinations(pruneLst, 3))
    pruneSet4 = set(combinations(pruneLst, 4))
    allSets   = set.union(pruneSet0,pruneSet1,pruneSet2,pruneSet3,pruneSet4)
    ###########################################################

    puzDicKeys = [ k for k in puzzlesDict.keys() ]
    print()
    for ii,k in enumerate(puzDicKeys):
        print('  {:2} - {}'.format( ii,k ))
    print( '   a - all')
    print( '   q - quit')
    puzIdxs = input('\n Choice -> ' ).split()

    if 'q' in puzIdxs:
        sys.exit()

    if 'a' in puzIdxs:
        dsrdKeys = [ puzDicKeys[    x ] for x in range(len(puzDicKeys))]
    else:
        dsrdKeys = [ puzDicKeys[int(x)] for x in puzIdxs]
    ###########################################################

    characterize = True
    characterize = False

    guess = True
    #guess = False

    if characterize and guess:
        print('\n  ERROR. Can\'t characterize and guesss together.\n')
        exit()

    if characterize: clArgs = allSets
    else: clArgs = [pruneLst]

    cumAllStr = ''
    cumSumStr = ''
    ###########################################################

    for pNme in dsrdKeys:
        pDat = puzzlesDict[pNme]
        for args in clArgs:
            puzzlesDict[pNme] = solvePuzzle(pDat, args)
            aStr, sStr = pr.printResults(pNme, pDat)
            cumAllStr += aStr
            cumSumStr += sStr

            if not puzzlesDict[pNme]['passed'] and guess == True:
                print('{} guessing'.format(pNme))
                input()
                tryCords, tryVals = \
                getGuesses(puzzlesDict[pNme]['solution'])
            
                for tVals in tryVals:
                    puzzlesDict[pNme]['guesses'] += 1
                    for ii,k in enumerate(tryCords):
                        puzzlesDict[pNme]['puzzle'][k[0]][k[1]] = tVals[ii]
            
                    puzzlesDict[pNme] = solvePuzzle(pDat, args)
                    aStr, sStr = pr.printResults(pNme, pDat)
                    cumAllStr += aStr
                    cumSumStr += sStr
                    if puzzlesDict[pNme]['passed']:
                        break

                for ii,k in enumerate(tryCords):
                    puzzlesDict[pNme]['puzzle'][k[0]][k[1]] = 0

    print(cumAllStr)
    print(cumSumStr)

    if characterize:
        with open('pData.txt', 'w', encoding='utf-8') as pFile:
            pFile.write(cumSumStr)
        an.analyze()

    endTime = time.time()
    print('Execution time = {:7.2f} seconds.'.format(endTime-startTime))


