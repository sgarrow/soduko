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

