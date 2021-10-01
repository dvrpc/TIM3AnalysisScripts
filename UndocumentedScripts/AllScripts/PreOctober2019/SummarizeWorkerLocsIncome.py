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

def cat_income(income):
    income = int(income)
    if income == -1:
        return '-1'
    elif income <= 15000:
        return '1'
    elif income <= 50000:
        return '2'
    elif income <= 75000:
        return '3'
    else:
        return '4'

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

data = {'1': init_od_table(counties),
        '2': init_od_table(counties),
        '3': init_od_table(counties),
        '4': init_od_table(counties)}

ke1 = 0
ke2 = 0
ke3 = 0
ke4 = 0
###############################################

wd = os.getcwd()
hh_file = os.path.join(wd, '_household_2.dat')
per_file = os.path.join(wd, '_person_2.dat')

hh2taz = {} #Household to taz
hh2inc = {} #Household to income

hh = open(hh_file, 'r')
first_line = True
for line in hh:
    entry = line.split('\t')
    if first_line:
        hhno = entry.index('hhno')
        hhtaz = entry.index('hhtaz')
        hhincome = entry.index('hhincome')
        first_line = False
    else:
        hh2taz[entry[hhno]] = entry[hhtaz]
        hh2inc[entry[hhno]] = cat_income(entry[hhincome])

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
            hcounty = taz2cnty[htaz]
        except KeyError:
            ke2 += 1
            continue
        try:
            hhinc = hh2inc[entry[hhno]]
        except KeyError:
            ke4 += 1
            continue
        try:
            wcounty = taz2cnty[entry[wtaz]]
        except KeyError:
            ke3 += 1
            continue
        #import pdb
        #pdb.set_trace()
        data[hhinc][hcounty][wcounty] += float(entry[psexpfac])

print 'Household number to household TAZ:   {}'.format(ke1)
print 'Household number to income category: {}'.format(ke4)
print 'Household TAZ to household county:   {}'.format(ke2)
print 'Work TAZ to work county:             {}'.format(ke3)
print 'Total Key Errors:                    {}'.format(ke1 + ke2 + ke3 + ke4)
print 'Total worker entries:                {}'.format(i)

###############################################

lines = {'1': [','.join([''] + counties)],
         '2': [','.join([''] + counties)],
         '3': [','.join([''] + counties)],
         '4': [','.join([''] + counties)]}
for pptyp in data:
    for ocounty in counties:
        line = [ocounty]
        for dcounty in counties:
            line.append(str(data[pptyp][ocounty][dcounty]))
        lines[pptyp].append(','.join(line))

outfile = {'1': r'D:\Debugging\WorkLocationInc0-15CountyFlow.csv',
           '2': r'D:\Debugging\WorkLocationInc15-50CountyFlow.csv',
           '3': r'D:\Debugging\WorkLocationInc50-75CountyFlow.csv',
           '4': r'D:\Debugging\WorkLocationInc100-infCountyFlow.csv'}

for pptyp in data:
    with open(outfile[pptyp], 'w') as f:
        f.write('\n'.join(lines[pptyp]))
        f.close()

Popen(outfile, shell = True)

#lines = data.split('\n')
#print lines[0]

#for char in data:
#    print char
