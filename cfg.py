import pprint as pp
import pickle
import sys
#############################################################################

def mkCfgDictPikleFile():
    cfgDict = {}
    rspStr  = ''
    error   = False
    try:
        with open('cfgFile.txt', 'r', encoding='utf-8') as f:
            for line in f:
                # If not a comment line and line is not all whitespace
                if '#' not in line and line.strip():
                    lSplit = line.split()
                    if lSplit[0] == 'key=':
                        cfgDict[ lSplit[1] ] = \
                            { 
                              'enabled'     : int( lSplit[2] ),
                              'isPrundFunc' : int( lSplit[3] ),
                              'prnLevel'    : int( lSplit[4] ),
                              'notes'       : ' '.join(lSplit[5:])
                            }

        with open('cfgFile.pickle', 'wb') as handle:
            pickle.dump(cfgDict, handle)
        rspStr += ' SUCCESS. File config dict saved to cfgFile.pickle.'

    except FileNotFoundError:
        error   = True
        rspStr += ' ERROR. File cfgFile.txt not found.'

    return error, rspStr, cfgDict
#############################################################################

if __name__ == '__main__':

    mnError, mnRspStr, mnCfgDict = mkCfgDictPikleFile()

    print(mnRspStr)
    if not mnError:
        with open('cfgFile.pickle', 'rb') as handle:
            mnCfgDict = pickle.load(handle)
        pp.pprint(mnCfgDict)
