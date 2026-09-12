def flatten(inLst):
    outLst = []
    for elem in inLst:
        try:
            for subEl in elem:
                outLst.append(subEl)
        except TypeError:
            outLst.append(elem)
    return outLst
#############################################################################

def genHistogram(inLst):
    hist = []
    for histBin in range(min(inLst), max(inLst)+1):
        binHeight = len([1 for x in inLst if x==histBin])
        if binHeight > 0:
            hist.append((histBin, binHeight))
    return hist
#############################################################################

