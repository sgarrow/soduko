def convert(inLstOfStrs):
   p1 = []
   for el in inLstOfStrs:
    p1.append([ int(ch) for ch in el ])
   return(p1)


#easy
puzEsy = [ '000005900',
           '890300006',
           '000829700',
           '040017029',
           '209436807',
           '560980010',
           '005168000',
           '900003068',
           '601200000' ]
#medium
puzMed = [ '000010000',
           '000389261',
           '061020000',
           '600850710',
           '100000004',
           '002001098',
           '800502000',
           '509000803',
           '000038045' ]
#hard
puzHrd = [ '904530600',
           '000040000',
           '000027004',
           '560070900',
           '009100706',
           '370900001',
           '032000100',
           '005008009',
           '000050040' ]
#expert
puzExp = [ '000476000',
           '000005800',
           '000001509',
           '000000004',
           '460000050',
           '070010006',
           '500030000',
           '009000231',
           '001700000' ]

#evil
puzEvl = [ '000390005',
           '028006100',
           '400000000',
           '063008200',
           '070000000',
           '000200010',
           '700000300',
           '100004000',
           '034060090' ]

#evil2
puzEv2 = [ '106000030',
           '020018400',
           '000700000',
           '300075040',
           '000200700',
           '050900000',
           '000009000',
           '080054100',
           '200000008' ]

#evil3
puzEv3 = [ '100000000',
           '000008603',
           '040050010',
           '051306000',
           '900000820',
           '000000000',
           '000000002',
           '400075000',
           '203040085' ]
# X-Wings
puzXW  = [ '100000569',
           '492056108',
           '056109240',
           '009640801',
           '064010000',
           '218035604',
           '040500016',
           '905061402',
           '621000005' ]

#hardest evr
puzWtf = [ '800000000',
           '003600000', # 94 is first 2. <--1
           '070090200',
           '050007000',
           '000045700', #  6 is second.  <--1
           '000100030',
           '001000068',
           '008500010',
           '090000400' ]

puzzlesDict = {

    'puzzleEsy' : { 'puzzle' : convert(puzEsy), 'solution' : [], 'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},

    'puzzleMed' : { 'puzzle' : convert(puzMed), 'solution' : [], 'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},
    
    'puzzleHrd' : { 'puzzle' : convert(puzHrd), 'solution' : [], 'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},
    
    'puzzleExp' : { 'puzzle' : convert(puzExp), 'solution' : [], 'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},
    
    'puzzleEvl' : { 'puzzle' : convert(puzEvl), 'solution' : [], 'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},
    
    'puzzleEv2' : { 'puzzle' : convert(puzEv2), 'solution' : [], 'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},
    
    'puzzleWtf' : { 'puzzle' : convert(puzWtf), 'solution' : [], 'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},
    
    'puzzleEv3' : { 'puzzle' : convert(puzEv3), 'solution' : [], 'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},
    
    'puzzleXW'  : { 'puzzle' : convert(puzXW),  'solution' : [], 'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},
    }

if __name__ == '__main__':
    print(puzzlesDict)
