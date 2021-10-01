from subprocess import Popen
import os

def add_to_list(item, lst):
    if item not in lst:
        lst.append(item)

def init_od_table(locs):
    od = {}
    for oloc in locs:
        od[oloc] = {}
        for dloc in locs:
            od[oloc][dloc] = 0
    return od

taz2cnty_file = r'D:\Debugging\taz2county.csv'
taz2cnty = {}
m = open(taz2cnty_file)
first_line = True
for line in m:
    if first_line:
        first_line = False
        continue
    county = line.split(',')[1].replace('\n', '')
    taz2cnty[line.split(',')[0]] = county

counties = []
fips2cnty_file = r'D:\Debugging\fips2county.csv'
fips2cnty = {}
f = open(fips2cnty_file)
first_line = True
for line in f:
    if first_line:
        first_line = False
        continue
    fips = line.split(',')[0]
    county = line.split(',')[1].replace('\n', '')
    fips2cnty[fips] = county
##    if county not in counties:
##        counties.append(county)

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

data = {'1': init_od_table(counties),
        '2': init_od_table(counties)}

ke1 = 0
ke2 = 0
ke3 = 0
###############################################

wd = os.getcwd()
hh_file = os.path.join(wd, '_household_2.dat')
per_file = os.path.join(wd, '_person_2.dat')

hh2taz = {} #Household to microzone

hh = open(hh_file, 'r')
first_line = True
for line in hh:
    entry = line.split('\t')
    if first_line:
        hhno = entry.index('hhno')
        hhtaz = entry.index('hhtaz')
        first_line = False
    else:
        hh2taz[entry[hhno]] = entry[hhtaz]

not_in_file = []

per = open(per_file, 'r')
first_line = True
i = 0
for line in per:
    entry = line.replace('\n', '').split('\t')
    if first_line:
        hhno = entry.index('hhno')
        pptyp = entry.index('pptyp')
        wtaz = entry.index('pwtaz')
        psexpfac = entry.index('psexpfac')
        first_line = False
    else:
        if entry[pptyp] not in data.keys() or entry[wtaz] == '-1':
            continue
        else:
            i += 1
        try:
            htaz = hh2taz[entry[hhno]]
        except KeyError:
            ke1 += 1
            continue
        try:
            hcounty = fips2cnty[taz2cnty[htaz]]
        except KeyError:
            ke2 += 1
            continue
        try:
            wcounty = fips2cnty[taz2cnty[entry[wtaz]]]
        except KeyError:
            ke3 += 1
            continue
        #import pdb
        #pdb.set_trace()
        data[entry[pptyp]][hcounty][wcounty] += float(entry[psexpfac])

print 'Household number to household TAZ: {}'.format(ke1)
print 'Household TAZ to household county: {}'.format(ke2)
print 'Work TAZ to work county:           {}'.format(ke3)
print 'Total Key Errors:                  {}'.format(ke1 + ke2 + ke3)
print 'Total worker entries:              {}'.format(i)

###############################################

lines = {'1': [','.join([''] + counties)],
         '2': [','.join([''] + counties)]}
for pptyp in data:
    for ocounty in counties:
        line = [ocounty]
        for dcounty in counties:
            line.append(str(data[pptyp][ocounty][dcounty]))
        lines[pptyp].append(','.join(line))

outfile = {'1': r'D:\Debugging\WorkLocationFullTimeCountyFlow.csv',
           '2': r'D:\Debugging\WorkLocationPartTimeCountyFlow.csv'}

for pptyp in data:
    with open(outfile[pptyp], 'w') as f:
        f.write('\n'.join(lines[pptyp]))
        f.close()

#Popen(outfile, shell = True)

#lines = data.split('\n')
#print lines[0]

#for char in data:
#    print char
