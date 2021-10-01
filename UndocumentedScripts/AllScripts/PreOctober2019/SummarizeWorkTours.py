from subprocess import Popen

def add_to_list(item, lst):
    if item not in lst:
        lst.append(item)

taz2cnty_file = r'D:\Debugging\taz2county.csv'
taz2cnty = {}
counties = []
m = open(taz2cnty_file)
for line in m:
    county = line.split(',')[1].replace('\n', '')
    taz2cnty[line.split(',')[0]] = county
    if county not in counties:
        counties.append(county)

fp = r'D:\Debugging\_tour_2.dat'
f = open(fp, 'r')

#h2w = []

countyod = {}
for ocounty in counties:
    countyod[ocounty] = {}
    for dcounty in counties:
        countyod[ocounty][dcounty] = 0

mzs = []
bad_mz = []
unassigned_trips = 0
i = 0
ke = 0
first_line = True
for line in f:
    if first_line:
        header = line.split('\t')
        pdpurp = header.index('pdpurp')
        topcl = header.index('topcl')
        tdpcl = header.index('tdpcl')
        totaz = header.index('totaz')
        tdtaz = header.index('tdtaz')
        toexpfac = header.index('toexpfac\n')
        first_line = False

    else:
        entry = line.split('\t')
        if entry[pdpurp] == '1':
            i += 1
            #print i
##            h2w.append([entry[opcl],
##                        entry[dpcl],
##                        entry[otaz],
##                        entry[dtaz],
##                        int(entry[trexpfac][:-1])
##                        ])
            try:
                ocounty = taz2cnty[entry[totaz]]
            except KeyError:
                ke += 1
                #add_to_list(entry[topcl], bad_mz)
                unassigned_trips += int(entry[toexpfac].replace('\n', ''))
                continue
            
            try:
                dcounty = taz2cnty[entry[tdtaz]]
            except KeyError:
                ke += 1
                #add_to_list(entry[tdpcl], bad_mz)
                unassigned_trips += int(entry[toexpfac].replace('\n', ''))
                continue
            
            countyod[ocounty][dcounty] += int(entry[toexpfac].replace('\n', ''))
            
print '{0}/{1} KeyErrors with {2} unassigned trips'.format(ke, i, unassigned_trips)

lines = [','.join([''] + counties)]
for ocounty in counties:
    line = [ocounty]
    for dcounty in counties:
        line.append(str(countyod[ocounty][dcounty]))
    lines.append(','.join(line))

outfile = r'D:\Debugging\CountyCountyH2WTours.csv'
with open(outfile, 'w') as f:
    f.write('\n'.join(lines))
    f.close()

Popen(outfile, shell = True)

#lines = data.split('\n')
#print lines[0]

#for char in data:
#    print char
