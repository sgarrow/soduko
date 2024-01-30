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

puzUsr = [ '000320100',
           '800706000',
           '700090500',
           '600005000',
           '000000090',
           '290010040',
           '000000700', # solution -> start 0005
           '030070000',
           '005008001' ]

#hardest evr
puzMax = [ '800000000',
           '003600000', # 94 is first 2. <--1
           '070090200',
           '050007000',
           '000045700', #  6 is second.  <--1
           '000100030',
           '001000068',
           '008500010',
           '090000400' ]




puzzlesDict = {

    'puzEsy_38' : { 'puzzle' : convert(puzEsy), 'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},
    
    'puzMed_32' : { 'puzzle' : convert(puzMed), 'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},
    
    'puzHrd_29' : { 'puzzle' : convert(puzHrd), 'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},
    
    'puzExp_23' : { 'puzzle' : convert(puzExp), 'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},
    
    'puzEvl_23' : { 'puzzle' : convert(puzEvl), 'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},
    
    'puzEv2_23' : { 'puzzle' : convert(puzEv2), 'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},
    
    'puzEv3_23' : { 'puzzle' : convert(puzEv3), 'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},
    
    'puzXW_46'  : { 'puzzle' : convert(puzXW),  'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},
    
    'puzUsr'    : { 'puzzle' : convert(puzUsr), 'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},

    'puzMax_21' : { 'puzzle' : convert(puzMax), 'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0},
    
    }

if __name__ == '__main__':
    print(puzzlesDict)
