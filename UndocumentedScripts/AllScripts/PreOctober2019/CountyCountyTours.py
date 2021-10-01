from subprocess import Popen

def add_to_list(item, lst):
    if item not in lst:
        lst.append(item)

taz2cnty_file = r'D:\Debugging\taz2county.csv'
taz2cnty = {}
m = open(taz2cnty_file)
for line in m:
    county = line.split(',')[1].replace('\n', '')
    taz2cnty[line.split(',')[0]] = county

fips2cnty_file = r'D:\Debugging\fips2county.csv'
fips2cnty = {}
counties = []
f = open(fips2cnty_file)
first_line = False
for line in f:
    if first_line:
        first_line = True
        continue
    fips = line.split(',')[0]
    county = line.split(',')[1].replace('\n', '')
    fips2cnty[fips] = county

counties = ['Bucks',
            'Chester',
            'Delaware',
            'Montgomery',
            'Philadelphia',
            'Burlington',
            'Camden',
            'Gloucester',
            'Mercer',
            'Rest of PA',
            'Rest of NJ',
            'Rest of Outer Counties',
            'Outside'
            ]

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
        #mode = header.index('mode')
        #dorp = header.index('dorp')
        topcl = header.index('topcl')
        tdpcl = header.index('tdpcl')
        totaz = header.index('totaz')
        tdtaz = header.index('tdtaz')
        toexpfac = header.index('toexpfac\n')
        first_line = False

    else:
        entry = line.split('\t')
        #add_to_list(entry[opcl], mzs)
        #add_to_list(entry[dpcl], mzs)
##        if entry[dorp] == '1':
##            i += 1
            #print i
##            h2w.append([entry[opcl],
##                        entry[dpcl],
##                        entry[otaz],
##                        entry[dtaz],
##                        int(entry[trexpfac][:-1])
##                        ])
        try:
            ocounty = fips2cnty[taz2cnty[entry[totaz]]]
        except KeyError:
            ke += 1
            #print entry[otaz]
            #raise Exception
            #add_to_list(entry[opcl], bad_mz)
            unassigned_trips += int(entry[toexpfac].replace('\n', ''))
            continue
        
        try:
            dcounty = fips2cnty[taz2cnty[entry[tdtaz]]]
        except KeyError:
            ke += 1
            #add_to_list(entry[dpcl], bad_mz)
            unassigned_trips += int(entry[toexpfac].replace('\n', ''))
            continue
        
        countyod[ocounty][dcounty] += int(entry[toexpfac].replace('\n', ''))
            
print '{0}/{1} KeyErrors with {2} unassigned tours'.format(ke, i, unassigned_trips)

lines = [','.join([''] + counties)]
for ocounty in counties:
    line = [ocounty]
    for dcounty in counties:
        line.append(str(countyod[ocounty][dcounty]))
    lines.append(','.join(line))

outfile = r'D:\Debugging\CountyCountyVehicleTours.csv'
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
