import fillRoutines  as fr
from itertools import combinations
import pprint as pp
import printRoutines as pr
import mapping as mp

# map sqrs to rows -> Xcanidates
# 
# find all numbers in rows of Xcanidates that appear exactly twice 
# 
# if the nums that appear exactly twice are in cols 
# 0,1,2 or 3,4,5 of 6,7,8 then they are in the same row of canidates
# and hence are a 'row' pointing pair.
# 
# if the nums that appear exactly twice are in cols 
# 0,3,6 or 1,4,7 of 2,5,8 then they are in the same col of canidates
# and hence are a 'col' pointing pair.
#
# process the pointing pairs in canidates.

def prunePointingPairs(canidates):
    Xcanidates = mp.mapSrqsToRows(canidates)

    #printCanidates(canidates)
    #printCanidates(Xcanidates)

    numPruned = 0

    allBinsHeightTwo = []
    for row in Xcanidates:
        flatRow = fr.flatten(row)
        histRow = fr.genHistogram(flatRow)
        allBinsHeightTwo.append([ x[0] for x in histRow if x[1] == 2 and x[0] != 0])
    pp.pprint(allBinsHeightTwo)
    print()

    k = 0
    myD = {}
    for idx,lstOfVals in enumerate(allBinsHeightTwo):
        for val in lstOfVals:
            cols = [ c for c,lst in enumerate(Xcanidates[idx]) if lst != 0 and val in lst ]
            #print(' in row {}, {} appears exactly twice - cols {}'.format(idx, val, cols))
            myD[k] = { 'A_sqr':idx, 'B_idxs':cols, 'C_val':val,  }
            k += 1
    #pp.pprint(myD)

    k = 0
    ppD = {}
    for v in myD.values():
        #print(v)
        diff = v['B_idxs'][1] - v['B_idxs'][0]
        sameRem = v['B_idxs'][1]//3 == v['B_idxs'][0]//3
        if diff < 3 and sameRem:
            ppD[k] = v
        k += 1
    #pp.pprint(ppD)


    k = 0
    ppD2 = {}
    for v in ppD.values():
        r0,c0 = mp.getRowColFromSqrOffset(v['A_sqr'],v['B_idxs'][0])
        r1,c1 = mp.getRowColFromSqrOffset(v['A_sqr'],v['B_idxs'][1])
        if r0 != r1:
            print('SANITY CHECK')
            exit()
        print('    square {} has row pointing pair on row {} cols {},{} (val={})'.\
            format(v['A_sqr'],r0,c0,c1,v['C_val']))
        ppD2[k] = { 'aRow':r0, 'bCols':[c0,c1], 'cVal':v['C_val'] }
        k += 1
    pp.pprint(ppD2)

    rowsProcessed = []
    for v in ppD2.values():
        if v['aRow'] not in rowsProcessed:
            cols = [ x for x in range(9) if x not in v['bCols'] ]
            for c in cols:
                if canidates[v['aRow']][c] != 0 and v['cVal'] in canidates[v['aRow']][c]:
                    canidates[ v['aRow']][c].remove(v['cVal'])
                    print('    removed {} from {},{}'.\
                        format(v['cVal'], v['aRow'], c))
                    numPruned += 1


    #pr.printCanidates(canidates)
    return numPruned,canidates
############################################################################

