triplet = [1,2,3]

comb = [[1,4,7],[1,2,3,5,8],[6,9]]

# every list in comb has to have at least one member of the triplet in it

allHaveLeastOne = True
for c in comb:
    inter = set.intersection(set(triplet), c)
    if len(inter) == 0:
        allHaveLeastOne = False
        break
print(allHaveLeastOne)


