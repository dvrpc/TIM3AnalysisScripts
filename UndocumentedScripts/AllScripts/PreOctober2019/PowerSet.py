def PowerSet(inlist):
    N = len(inlist)
    outlist = [inlist]
    if N == 0:
        pass
    else:
        #outlist += ([inlist[1:]] + [inlist[:-1]] + PowerSet(inlist[1:]) + PowerSet(inlist[:-1]))
        outlist += [inlist[:-1]]
        outlist += [inlist[1:]]
        outlist += PowerSet(inlist[:-1])
        outlist += PowerSet(inlist[1:])
    
    #Remove duplicates
    duplicates = []
    for i in range(len(outlist)):
        if outlist[i] in outlist[:i]:
            duplicates += [i]
    duplicates.sort()
    duplicates.reverse()
    for ix in duplicates:
        del outlist[ix]

    outlist.sort(key = len)
    return outlist

a = ['a', 'b', 'c']
b = PowerSet(a)
print(b)