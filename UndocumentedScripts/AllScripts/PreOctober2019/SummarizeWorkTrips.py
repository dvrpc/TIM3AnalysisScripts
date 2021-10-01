from subprocess import Popen

def add_to_list(item, lst):
    if item not in lst:
        lst.append(item)

mz2cnty_file = r'D:\Debugging\mz2cnty.csv'
mz2cnty = {}
counties = []
m = open(mz2cnty_file)
for line in m:
    county = line.split(',')[1].replace('\n', '')
    mz2cnty[line.split(',')[0]] = county
    if county not in counties:
        counties.append(county)

fp = r'D:\Debugging\_trip_2.dat'
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
        opurp = header.index('opurp')
        dpurp = header.index('dpurp')
        opcl = header.index('opcl')
        dpcl = header.index('dpcl')
        otaz = header.index('otaz')
        dtaz = header.index('dtaz')
        trexpfac = header.index('trexpfac\n')
        first_line = False

    else:
        entry = line.split('\t')
        #add_to_list(entry[opcl], mzs)
        #add_to_list(entry[dpcl], mzs)
        if entry[opurp] == '0' and entry[dpurp] == '1':
            i += 1
            #print i
##            h2w.append([entry[opcl],
##                        entry[dpcl],
##                        entry[otaz],
##                        entry[dtaz],
##                        int(entry[trexpfac][:-1])
##                        ])
            try:
                ocounty = mz2cnty[entry[opcl]]
            except KeyError:
                ke += 1
                add_to_list(entry[opcl], bad_mz)
                unassigned_trips += int(entry[trexpfac].replace('\n', ''))
                continue
            
            try:
                dcounty = mz2cnty[entry[dpcl]]
            except KeyError:
                ke += 1
                add_to_list(entry[dpcl], bad_mz)
                unassigned_trips += int(entry[trexpfac].replace('\n', ''))
                continue
            
            countyod[ocounty][dcounty] += int(entry[trexpfac].replace('\n', ''))
            
print '{0}/{1} KeyErrors with {2} unassigned trips'.format(ke, i, unassigned_trips)

lines = [','.join([''] + counties)]
for ocounty in counties:
    line = [ocounty]
    for dcounty in counties:
        line.append(str(countyod[ocounty][dcounty]))
    lines.append(','.join(line))

outfile = r'D:\Debugging\CountyCountyH2W.csv'
with open(outfile, 'w') as f:
    f.write('\n'.join(lines))
    f.close()

Popen(outfile, shell = True)

##outfile = r'D:\Debugging\microzoneError.csv'
##lines = ['Microzone', 'KeyError']
##for mz in mzs:
##    if mz in bad_mz:
##        lines.append(['{},1'.format(mz)])
##    else:
##        lines.append(['{},0'.format(mz)])
##
##with open(outfile, 'w') as f:
##    f.write('\n'.join(lines))
##    f.close()

#lines = data.split('\n')
#print lines[0]

#for char in data:
#    print char
