import fillRoutines  as fr
from itertools import combinations
import pprint as pp
from itertools import combinations
import printRoutines as pr
import pprint as pp
import fillRoutines  as fr

def pruneHiddenTriplesRowOrCols(canidates, processRowsOrCols):

    import copy

    Xpos = [[row[i] for row in canidates] for i in range(len(canidates[0]))]

    if processRowsOrCols == 'row': Xcanidates = copy.deepcopy(canidates)
    else:                          Xcanidates = copy.deepcopy(Xpos)

    print('Pruning hidden triples ********************************* Start.')
    print('  Finding hidden triples in {}s.'.format(processRowsOrCols))

    numPruned = 0
    for idx, rowOrColWithZeros in enumerate(Xcanidates):
        rowOrCol     = [set(x) if x != 0 else set([0]) for x in rowOrColWithZeros]
        combSet      = combinations(rowOrCol, 3)  # C(n,r) = n! / ( r! * (n-r)! ). C(9,3) = 84.
        combIdxs     = list((i,j,k) for ((i,_),(j,_),(k,_)) in combinations(enumerate(rowOrCol), 3))
        #[ print(el) for el in combSet ]
        #pp.pprint (combIdxs)
        #print(rowOrCol)
        #exit()

        for comb,comIdx in zip(combSet,combIdxs):

            #[ print(el) for el in comb ]
            #print()
            if any( el == {0} for el in comb):
                #print('skipping')
                continue
            else:
                pass
                #print('processing')

            T   = comIdx
            Tc  = [ x for x in range(0,len(rowOrCol)) if x not in T ]
            H   = set.union( comb[0], comb[1], comb[2] )
            G   = set(fr.flatten([ rowOrCol[ii] for ii in Tc if rowOrCol[ii] != [0]]))
            HmG = list(H - G)
            NEW_hIsNaked  = (len(H) == 3)
            NEW_hIsHidden = (len(H) > 3) and (len(HmG) == 3)
    
            #print( '{}{}'.format(str(comb).ljust(40),comIdx) )
            #print('idx, T, Tcomp     = ', idx, T, Tc   )
            #print('idx, H, G         = ', idx, H, G   )
            #print('idx, Hmg   = ', idx, HmG )
            #print('idx ************* NEW_hIsNaked',  idx, NEW_hIsNaked  )
            #print('idx ************* NEW_hIsHidden', idx, NEW_hIsHidden )

            if NEW_hIsHidden:
                if processRowsOrCols == 'row':
                    print(' row {:2} has hidden triple {} in cols {}'.format(idx, HmG, comIdx))
                    myD = {'row': idx, 'tripVals': HmG, 'tripIdxs': comIdx}
                else:
                    print(' col {} has hidden triple {} in rows {}'.format(idx, HmG, comIdx))
                    myD = {'col': idx, 'tripVals': HmG, 'tripIdxs': comIdx}

                #print()
                #pr.prettyPrint3DArray(canidates)
                #print()
    
                for tripIdx in myD['tripIdxs']:
                    if processRowsOrCols == 'row':
                        temp = [ x for x in canidates[myD['row']][tripIdx] if x in myD['tripVals'] ]
                        inter5 = set.intersection( set(canidates[myD['row']][tripIdx]), set(temp) )
                        diff = set(canidates[myD['row']][tripIdx]) - inter5
                        if len(diff) != 0:
                            numPruned += len(diff)
                            print( '   Removed {} from row {} cols {}'.format(diff, myD['row'], myD['tripIdxs']) )
                        canidates[myD['row']][tripIdx] = temp
                    else:
                        temp = [ x for x in canidates[tripIdx][myD['col']] if x in myD['tripVals'] ]
                        inter5 = set.intersection( set(canidates[tripIdx][myD['col']]), set(temp) )
                        diff = set(canidates[tripIdx][myD['col']]) - inter5
                        if len(diff) != 0:
                            numPruned += len(diff)
                            print( '   Removed {} from col {} rows {}'.format(diff, myD['col'], myD['tripIdxs']) )
                        canidates[tripIdx][myD['col']] = temp
    
                #print()
                #pr.prettyPrint3DArray(canidates)
                #print()

                break

    print()
    print('Pruning hidden triples ** ( total pruned =  {} ) ******* End.'.format(numPruned))
    return(numPruned, canidates)

if __name__ == '__main__':
    canidates = \
    [
        [ [1,2,3],   [1,2,3],   [1,2,3],   [7],       [8],      [9]     ], #  0. 3/3/3
        [ [1,2,3],   [1,2,3],   [1,2],     [7],       [8],      [9]     ], #  1. 3/3/2
        [ [1,2,3],   [1,2],     [1,3],     [7],       [8],      [9]     ], #  2. 3/2/2
        [ [1,2],     [1,3],     [2,3],     [7],       [8],      [9]     ], #  3. 2/2/2
                                                                  # 
        [ [1,2,3,4], [1,2,3],   [1,2,3],   [7,4],     [8],      [9]     ], #  4. 3+/3/3
        [ [1,2,3,4], [1,2,3,5], [1,2,3],   [7,4,5],   [8],      [9]     ], #  5. 3+/3+/3
        [ [1,2,3,4], [1,2,3,5], [1,2,3,6], [7,4,5,6], [8],      [9]     ], #  6. 3+/3+/3+
                                                                  # 
        [ [1,2,3,4], [1,2,3],   [1,2],     [7,4],     [8],      [9]     ], #  7. 3+/3/2
        [ [1,2,3,4], [1,2,3,5], [1,2],     [7,4,5],   [8],      [9]     ], #  8. 3+/3+/2
        [ [1,2,3,4], [1,2,3,5], [1,2],     [7,4,5,6], [8],      [9]     ], #  9. 3+/3+/2+
        [ [1,2,3],   [1,2,3],   [1,2,4],   [7,4],     [8],      [9]     ], # 10. 3/3/2+
        [ [1,2,3,4], [1,2],     [1,3],     [7,4],     [8],      [9]     ], # 11. 3+/2/2
                                                                  # 
        [ [1,2,3,4], [1,2,5],   [1,3],     [7,4,5],   [8],      [9]     ], # 12. 3+/2+/2
        [ [1,2,3,4], [1,2,5],   [1,3,6],   [7,4,5,6], [8],      [9]     ], # 13. 3+/2+/2+
        [ [1,2,3],   [1,2,4],   [1,3,],    [7,4],     [8],      [9]     ], # 14. 3/2+/2
        [ [1,2,3],   [1,2,4],   [1,3,5],   [7,4,5],   [8],      [9]     ], # 15. 3/2+/2+
        
        [ [1,2,4],   [1,3],     [2,3],     [7,4],     [8],      [9]     ], # 16. 2+/2/2
        [ [1,2,4],   [1,3,5],   [2,3],     [7,4,5],   [8],      [9]     ], # 17. 2+/2+/2
        [ [1,2,4],   [1,3,5],   [2,3,6],   [7,4,5,6], [8],      [9]     ], # 18. 2+/2+/2+
        
        [ [1,2,3,4], [1,2,3,4], [1,2,3,4], [7,4],     [8],      [9]     ], # 19. 3+a/3+a/3+a - Not found. Ok, its a naked quad.
        [ [1,2,3,4], [1,2,3,4], [1,2,3,5], [7,4,5],   [8],      [9]     ], # 20. 3+a/3+a/3+b -
        [ [1,2,3,4], [1,2,3,5], [1,2,3,4], [7,4,5],   [8],      [9]     ], # 21. 3+a/3+b/3+a -
        [ [1,2,3,4], [1,2,3,5], [1,2,3,5], [7,4,5],   [8],      [9]     ], # 22. 3+a/3+b/3+b -
        [ [1,2,3,5], [1,2,3,4], [1,2,3,4], [7,4,5],   [8],      [9]     ], # 23. 3+b/3+a/3+a -
        [ [1,2,3,5], [1,2,3,4], [1,2,3,5], [7,4,5],   [8],      [9]     ], # 24. 3+b/3+a/3+b -
        [ [1,2,3,5], [1,2,3,5], [1,2,3,4], [7,4,5],   [8],      [9]     ], # 25. 3+b/3+b/3+a -
        [ [1,2,3,5], [1,2,3,5], [1,2,3,5], [7,5],     [8],      [9]     ], # 26. 3+b/3+b/3+b -
        
        [ [1,2,3,4], [1,2,3,5,6], [1,2,3,6],  [7],    [8],      [9]     ], # 27. 
        [ [1,2,3,4], [1,2,3,5],   [1,2,7],    [7],    [8],      [9]     ], # 28. 
        [ [1,2,3,4], [1,2,5],     [2,3,8],    [7],    [8],      [9]     ], # 29. 
        [ [1,2,4],   [1,3,5],     [2,3,9],    [7],    [8],      [9]     ], # 30. 
        [ [6,8,9],   [2,6,7,8,9], [6,8,9],    [5,7],  [2,7],    [2,5,7] ], # 31. 
        [ [1,2,3],   [1,4],       [2,5],      [7],    [8],      [9]     ], # 32. 
        
        [ [2,4,5,6,7,8], [2,4,5,6,7,8], [5,6,7],      [0],      [2],   [2,4,8] ], # 33.
        [ [1,3,7], [3,4,7], [3,4,7], [1,8],           [1,5,8],  [5,6], [1,6]   ], # 34.

        # hidden triple [0, 2, 3] in cols (0, 7, 8)
        [0,                  
         [5, 9],
         [5, 9],
         [1, 5, 7, 8],
         [1, 5, 7, 8],
         [1, 5, 7],
         [6, 7, 8, 9],
         [2, 3, 6, 7, 8],
         [2, 3, 6, 7, 8, 9]]
        
     ]

    #canidates = \
    #[
    #    [ [1,2,3,4], 0,0,0,0,0,0,0,0 ],
    #    [ [1,2,3,5], 0,0,0,0,0,0,0,0 ],
    #    [ [1,2,3,6], 0,0,0,0,0,0,0,0 ],
    #    [ [7,8,6],     0,0,0,0,0,0,0,0 ],
    #    [ [8,9],     0,0,0,0,0,0,0,0 ],
    #    [ [9,7],     0,0,0,0,0,0,0,0 ],
    # ]


    totNumPruned  = 0
    loopNumPruned = 1
    while loopNumPruned:
        loopNumPruned, canidates = pruneHiddenTriplesRowOrCols(canidates, 'row')
        totNumPruned  += loopNumPruned
    print('Total Pruning hidden triples ** ( total pruned =  {} ) ******* End.'.format(totNumPruned))
    #numPruned4, canidates = pruneHiddenTriplesRowOrCols(canidates, 'col')
