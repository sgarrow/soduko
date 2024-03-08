def analyze():
    #import pprint        as pp

    with open('pData.txt', encoding='utf-8') as pFile:
        lines = [line.rstrip().split() for line in pFile]
    #[print(line) for line in lines]

    mainD = {}
    for aLine in lines:
        puz  = aLine[0]
        sts  = aLine[1]

        prn1 = aLine[2:]
        prn2 = [ x.strip('\',()') for x in prn1 ]
        prn  = '_'.join(x for x in sorted(prn2))
        if prn == '': prn = '0'

        if puz not in mainD:
            mainD[puz] = { sts:[prn] }
        else:
            subD = mainD[puz]
            if sts not in subD:
                subD[sts] = [prn]
            else:
                subD[sts].append(prn)

    print()
    for k,v in mainD.items():
        if 'PASS' in v:
            minLen = (min([ len(x) for x in v['PASS']]))
            print(' {:9} can PASS w/ :'.format(k),end='')
            print([ x for x in v['PASS'] if len(x) == minLen])
        else:
            print(' {:9} always FAILS'.format(k))
    print()
