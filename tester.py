import fillRoutines  as fr
from itertools import combinations
import pprint as pp
from itertools import combinations
import printRoutines as pr
import pprint as pp
import fillRoutines  as fr

def pruneHiddenTriplesRows(canidates):

    print('Pruning hidden triples ********************************* Start.')
    print('  Finding hidden triples in rows.')
    hiddenTrpiD = {}
    itemNum = 0
    for idx, rowWithZeros in enumerate(canidates):
        row         = [x if x != 0 else [0] for x in rowWithZeros]
        combSet     = list(combinations(row, 3))  # C(n,r) = n! / ( r! * (n-r)! ). C(9,3) = 84.
        combLst     = [ list(el) for el in combSet ]
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
            unionLst = list(union)
            numZeroLen = interLen.count(0)
            numOneLen  = interLen.count(1)
    
            #print( '{}{}'.format(str(comb).ljust(40),comIdx) )
            #print( 'intersections        = ', inter1,inter2,inter3,inter4 )
            #print( 'lenIntersections     = ', interLen )
            #print( 'unionOfIntersections = ', union )
            #print( 'lenUnion  numZeroLengthInter  numOneLengthInter  = {} {} {}'.format(unionLen, numZeroLen, numOneLen))

            empiricallyPotential     = False # 1. Determined empirically.
            valsCorrectNumOccurances = True  # 2. Defn ... appear allowable number of times (<3).
            valsCorrectPlacement     = True  # 3. Defn ... appear only in the 3 cols of the comb in question. 

            if [ unionLen, numZeroLen, numOneLen ] == [ 3,0,0 ]: empiricallyPotential = True # Potential hidden triplet type - 3/3/3 or 3/3/2.
            if [ unionLen, numZeroLen, numOneLen ] == [ 3,0,2 ]: empiricallyPotential = True # Potential hidden triplet type - 3/2/2.
            if [ unionLen, numZeroLen, numOneLen ] == [ 3,1,3 ]: empiricallyPotential = True # Potential hidden triplet type - 2/2/2. 

            for el in unionLst:
                flatRow = fr.flatten(row)
                if flatRow.count(el) > 3:
                    valsCorrectNumOccurances = False
                    break

            # cols each element in this combinations set intersetsion/union the union appears
            allIdxs = []
            for elInUnion in unionLst:
                idxs = [ idx for idx,el in enumerate(row) if elInUnion in el]
                allIdxs.append(idxs)
            #print(allIdxs)
            # Now make sure they only appear in the right places.
            for idxs in allIdxs:
                for currIdx in idxs:
                    if currIdx not in comIdx:
                        valsCorrectPlacement = False
                        break
                    if valsCorrectPlacement == False:
                        break


            #print(empiricallyPotential, valsCorrectNumOccurances, valsCorrectPlacement)
            isHiddenTrip = False
            if empiricallyPotential and valsCorrectNumOccurances and valsCorrectPlacement:
                isHiddenTrip = True
    
            if isHiddenTrip:
                print(' row {} has hidden triple {} in cols {}'.format(idx,union, comIdx))
                myD = {'row': idx, 'tripVals': unionLst, 'tripIdxs': comIdx}
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
    print('numPruned = {}'.format(numPruned))


    print()
    pr.prettyPrint3DArray(canidates)
    print()
    print('Pruning hidden triples ** ( total pruned =  {} ) ******* End.'.format(numPruned))
    return(numPruned, canidates)

if __name__ == '__main__':
    canidates = \
    [
        [  [1,2,3,4], [1,2,3,5], [1,2,3,6], [7,8],  [8,9], [9,7] ],
        [  [1,2,3,4], [1,2,3,5], [1,2,7],   [7],    [8],   [9]   ],
        [  [1,2,3,4], [1,2,5],   [2,3,8],   [7],    [8],   [9]   ],
        [  [1,2,4],   [1,3,5],   [2,3,9],   [7],    [8],   [9]   ],
         
        #     *        6             *        *    Not a triple.
        [  [1, 6, 8], [4, 8],    [1, 3],    [3, 6], 0,     0     ]
     ]
    numPruned4, canidates = pruneHiddenTriplesRows(canidates)
