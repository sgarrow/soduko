from itertools import combinations
import printRoutines as pr
import pprint as pp
import fillRoutines  as fr

def pruneHiddenTriplesRows(canidates):

    #canidates = \
    #[
    #    [  [1,2,3,4], [1,2,3,5], [1,2,3,6],  [7,8],[8,9],[9,7] ], # 3/3/3, 2/2/2
    #    [  [1,2,3,4], [1,2,3,5], [1,2,7],    [7],[8],[9]       ], # 3/3/2
    #    [  [1,2,3,4], [1,2,5],   [2,3,8],    [7],[8],[9]       ], # 3/2/2
    #    [  [1,2,4],   [1,3,5],   [2,3,9],    [7],[8],[9]       ], # 2/2/2
    #]

    print('Pruning hidden triples ********************************* Start.')
    print('  Finding hidden triples in rows.')
    hiddenTrpiD = {}
    itemNum = 0
    for idx, rowWithZeros in enumerate(canidates):
        row         = [x if x != 0 else [0] for x in rowWithZeros]
        comb        = list(combinations(row, 3))  # C(n,r) = n! / ( r! * (n-r)! ). C(9,3) = 84.
        combLst     = [ list(el) for el in comb ]
        combIdxs    = list((i,j,k) for ((i,_),(j,_),(k,_)) in combinations(enumerate(row), 3))
        combIdxsLst = [ list(el) for el in combIdxs ]
        #pp.pprint (combLst)
        #pp.pprint (combIdxsLst)
    
        #print('**********************************************************')
        #print(row)
        
        for comb,comIdx in zip(combLst,combIdxsLst):
            inter1 = set.intersection( set(comb[0]), set(comb[1]), set(comb[2]) )
            inter2 = set.intersection( set(comb[0]), set(comb[1]) )
            inter3 = set.intersection( set(comb[0]), set(comb[2]) )
            inter4 = set.intersection( set(comb[1]), set(comb[2]) )
            union  = set.union( inter1, inter2, inter3, inter4 )
            interLen = [ len(inter1),len(inter2),len(inter3),len(inter4) ]
            unionLen = len(union)
            numZeroLen = interLen.count(0)
            numOneLen  = interLen.count(1)
    
            #print( '{}{}'.format(str(comb).ljust(40),comIdx) )
            #print( 'intersections        = ', inter1,inter2,inter3,inter4 )
            #print( 'lenIntersections     = ', interLen )
            #print( 'unionOfIntersections = ', union )
            #print( 'lenUnion  numZeroLengthInter  numOneLengthInter  = {} {} {}'.format(unionLen, numZeroLen, numOneLen))

            potential = False
            if [ unionLen, numZeroLen, numOneLen ] == [ 3,0,0 ]: potential = True # Potential hidden triplet type - 3/3/3 or 3/3/2.
            if [ unionLen, numZeroLen, numOneLen ] == [ 3,0,2 ]: potential = True # Potential hidden triplet type - 3/2/2.
            if [ unionLen, numZeroLen, numOneLen ] == [ 3,1,3 ]: potential = True # Potential hidden triplet type - 2/2/2. 

            if potential:
                unionLst = list(union)
                for el in unionLst:
                    isHiddenTrip = True
                    flatRow = fr.flatten(row)
                    if flatRow.count(el) > 3:
                        isHiddenTrip = False
                        break
    
                if isHiddenTrip:
                    #print('row {} has hidden triple {} in cols {}'.format(idx,union, comIdx))
                    myD = {'row': idx, 'tripVals': list(union), 'tripIdxs': comIdx}
                    hiddenTrpiD[itemNum] = myD
                    itemNum += 1

    print()
    pp.pprint(hiddenTrpiD)

    print()
    pr.prettyPrint3DArray(canidates)
    print()

    numPruned = 0
    for dEntry in hiddenTrpiD.values():
        for idx in dEntry['tripIdxs']:
            temp = [ x for x in canidates[dEntry['row']][idx] if x in dEntry['tripVals'] ]
            inter5 = set.intersection( set(canidates[dEntry['row']][idx]), set(temp) )
            diff = set(canidates[dEntry['row']][idx]) - inter5
            if len(diff) != 0:
                numPruned += len(diff)
                print( '   Removed {} from row {} cols {}, where present'.format(diff, dEntry['row'], dEntry['tripIdxs']) )
            canidates[dEntry['row']][idx] = temp
        print()
    print()
    #print('numPruned = {}'.format(numPruned))


    print()
    pr.prettyPrint3DArray(canidates)
    print()
    print('Pruning hidden triples ** ( total pruned =  {} ) ******* End.'.format(numPruned))
    return(numPruned, canidates)

