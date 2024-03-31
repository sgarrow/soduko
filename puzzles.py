def convert(inLstOfStrs):
    allLines = []
    for el in inLstOfStrs:
        allLines.append([ int(ch) for ch in el if ch != ' ' ])
    return allLines
#############################################################################

puzEsy = [ '000 005 900',
           '890 300 006',
           '000 829 700',

           '040 017 029',
           '209 436 807',
           '560 980 010',

           '005 168 000',
           '900 003 068',
           '601 200 000' ]
puzMed = [ '000 010 000',
           '000 389 261',
           '061 020 000',

           '600 850 710',
           '100 000 004',
           '002 001 098',

           '800 502 000',
           '509 000 803',
           '000 038 045' ]
puzHrd = [ '904 530 600',
           '000 040 000',
           '000 027 004',

           '560 070 900',
           '009 100 706',
           '370 900 001',

           '032 000 100',
           '005 008 009',
           '000 050 040' ]
puzExp = [ '000 476 000',
           '000 005 800',
           '000 001 509',

           '000 000 004',
           '460 000 050',
           '070 010 006',

           '500 030 000',
           '009 000 231',
           '001 700 000' ]

puzEvl = [ '000 390 005',
           '028 006 100',
           '400 000 000',

           '063 008 200',
           '070 000 000',
           '000 200 010',

           '700 000 300',
           '100 004 000',
           '034 060 090' ]

puzEv2 = [ '106 000 030',
           '020 018 400',
           '000 700 000',

           '300 075 040',
           '000 200 700',
           '050 900 000',

           '000 009 000',
           '080 054 100',
           '200 000 008' ]

puzEv3 = [ '100 000 000',
           '000 008 603',
           '040 050 010',

           '051 306 000',
           '900 000 820',
           '000 000 000',

           '000 000 002',
           '400 075 000',
           '203 040 085' ]
puzXW1 = [ '100 000 569',
           '492 056 108',
           '056 109 240',

           '009 640 801',
           '064 010 000',
           '218 035 604',

           '040 500 016',
           '905 061 402',
           '621 000 005' ]
puzYW1 = [ '091 700 050',
           '700 801 000',
           '008 469 000',

           '073 000 000',
           '000 396 000',
           '000 000 280',

           '000 684 500',
           '000 902 001',
           '020 007 940' ]

puzYW2 = [ '007 000 400',
           '060 070 030',
           '090 203 000',

           '005 047 609',
           '000 000 000',
           '908 130 200',

           '000 705 080',
           '070 020 090',
           '001 000 500' ]

puzUsr = [ '000 320 100',
           '800 706 000',
           '700 090 500',

           '600 005 000',
           '000 000 090',
           '290 010 040',

           '000 000 700',
           '030 070 000',
           '005 008 001' ]

puzImp_28=['601 080 092',
           '900 000 410',
           '080 009 700',

           '006 002 000',
           '500 000 001',
           '000 400 500',

           '032 600 050',
           '890 000 006',
           '100 030 204' ]

puzMax = [ '800 000 000',
           '003 600 000',
           '070 090 200',

           '050 007 000',
           '000 045 700',
           '000 100 030',

           '001 000 068',
           '008 500 010',
           '090 000 400' ]
#############################################################################

puzzlesDict = {

    'puzEsy_38' : { 'puzzle' : convert(puzEsy), 'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0,
                    'prunes': None, 'passed': None, 'guesses': 0},

    'puzMed_32' : { 'puzzle' : convert(puzMed), 'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0,
                    'prunes': None, 'passed': None, 'guesses': 0},

    'puzHrd_29' : { 'puzzle' : convert(puzHrd), 'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0,
                    'prunes': None, 'passed': None, 'guesses': 0},

    'puzExp_23' : { 'puzzle' : convert(puzExp), 'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0,
                    'prunes': None, 'passed': None, 'guesses': 0},

    'puzEvl_23' : { 'puzzle' : convert(puzEvl), 'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0,
                    'prunes': None, 'passed': None, 'guesses': 0},

    'puzEv2_23' : { 'puzzle' : convert(puzEv2), 'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0,
                    'prunes': None, 'passed': None, 'guesses': 0},

    'puzEv3_23' : { 'puzzle' : convert(puzEv3), 'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0,
                    'prunes': None, 'passed': None, 'guesses': 0},

    'puzXW1_46' : { 'puzzle' : convert(puzXW1),  'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0,
                    'prunes': None, 'passed': None, 'guesses': 0},

    'puzYW1_29' : { 'puzzle' : convert(puzYW1),  'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0,
                    'prunes': None, 'passed': None, 'guesses': 0},

    'puzYW2_26' : { 'puzzle' : convert(puzYW2),  'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0,
                    'prunes': None, 'passed': None, 'guesses': 0},

    'puzUsr_22' : { 'puzzle' : convert(puzUsr), 'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0,
                    'prunes': None, 'passed': None, 'guesses': 0},

    'puzImp_28' : { 'puzzle' : convert(puzImp_28),'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0,
                    'prunes': None, 'passed': None, 'guesses': 0},

    'puzMax_21' : { 'puzzle' : convert(puzMax), 'solution' : [],
                    'start0s' : 0, 'end0s' : 0,
                    'oC' : 0, 'oR' : 0, 'rC' : 0, 'rR' : 0,
                    'cC' : 0, 'cR' : 0, 'sC' : 0, 'sR' : 0,
                    'prunes': None, 'passed': None, 'guesses': 0},

    }

if __name__ == '__main__':
    print(puzzlesDict)
