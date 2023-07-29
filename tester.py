import fillRoutines  as fr
from itertools import combinations
import pprint as pp

if __name__ == '__main__':

    canidates = \
    [
        [  [1,2,3,4], [1,2,3,5], [1,2,3,6],  [7,8],[8,9],[9,7]  ], # 3/3/3
        [  [1,2,3,4], [1,2,3,5], [1,2,6],    [7],[8],[9]      ], # 3/3/2
        [  [1,2,3,4], [1,2,5],   [2,3,6],    [7],[8],[9]      ], # 3/2/2
        [  [1,2,4],   [1,3,5],   [2,3,6],    [7],[8],[9]      ], # 2/2/2
    ]


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
