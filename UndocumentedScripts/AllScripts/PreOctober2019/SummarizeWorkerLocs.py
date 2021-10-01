from subprocess import Popen
import os

def add_to_list(item, lst):
    if item not in lst:
        lst.append(item)

taz2cnty_file = r'D:\Debugging\taz2county.csv'
taz2cnty = {}
counties = []
m = open(taz2cnty_file)
first_line = True
for line in m:
    if first_line:
        first_line = False
        continue
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
        wtaz = entry.index('pwtaz')
        psexpfac = entry.index('psexpfac')
        first_line = False
    else:
        if entry[wtaz] == '-1':
            continue
        else:
            i += 1
        try:
            htaz = hh2taz[entry[hhno]]
        except KeyError:
            ke1 += 1
            continue
        try:
            hcounty = taz2cnty[htaz]
        except KeyError:
            ke2 += 1
            #add_to_list(htaz, not_in_file)
            continue
        try:
            wcounty = taz2cnty[entry[wtaz]]
        except KeyError:
            #print entry[wtaz]
            ke3 += 1
            #add_to_list(entry[wtaz], not_in_file)
            continue
        countyod[hcounty][wcounty] += float(entry[psexpfac])

print 'Household number to household TAZ: {}'.format(ke1)
print 'Household TAZ to household county: {}'.format(ke2)
print 'Work TAZ to work county:           {}'.format(ke3)
print 'Total Key Errors:                  {}'.format(ke1 + ke2 + ke3)
print 'Total worker entries:              {}'.format(i)

###############################################

lines = [','.join([''] + counties)]
for ocounty in counties:
    line = [ocounty]
    for dcounty in counties:
        line.append(str(countyod[ocounty][dcounty]))
    lines.append(','.join(line))

outfile = r'D:\Debugging\WorkLocationCountyFlow.csv'
with open(outfile, 'w') as f:
    f.write('\n'.join(lines))
    f.close()

Popen(outfile, shell = True)

#lines = data.split('\n')
#print lines[0]

#for char in data:
#    print char
