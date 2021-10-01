import os
from collections import OrderedDict

#base_path = r'T:\TIM_3.1\190712_FullTest\scenario\Output'
#hh_file = os.path.join(base_path, '_household_2.dat')
base_path = r'D:\TIM3\SurveyData'
hh_file = os.path.join(base_path, 'dvrpc_hrecx4.dat')
taz_file = os.path.join(base_path, 'taz2county.csv')
outfile = os.path.join(base_path, 'VehOwnershipByCounty.csv')

#Create dictionary to map TAZ to CPA
taz2county = {}
f = open(taz_file, 'r')
lines = f.read().split('\n')
f.close()

for line in lines[1:-1]:
    taz_county_pair = line.split(',')
    taz2county[taz_county_pair[0]] = (taz_county_pair[1])

counties = ['Philadelphia', 'Delaware', 'Chester', 'Montgomery', 'Bucks', 'Mercer', 'Burlington', 'Camden', 'Gloucester', 'Rest of PA', 'Rest of NJ', 'Rest of Outer Counties']
vehs = [str(i) for i in range(16)]

f = open(hh_file, 'r')
lines = f.read().split('\n')
f.close()

delimiter = ','

header = lines[0].split(delimiter)
hhtaz = header.index('hhtaz')
hhvehs = header.index('hhvehs')
hhexpfac = header.index('hhexpfac')

outdata = OrderedDict()
for county in counties:
    outdata[county] = OrderedDict()
    for veh in vehs:
        outdata[county][veh] = 0.0

for line in lines[1:-1]:
    hh = line.split(delimiter)

    hhcounty = taz2county[hh[hhtaz]]
    veh = hh[hhvehs]
    outdata[hhcounty][veh] += float(hh[hhexpfac])

lines = ['County,' + ','.join(vehs)]
for county in counties:
    new_line = county + ','
    new_line += ','.join(str(outdata[county][veh]) for veh in vehs)
    lines.append(new_line)

f = open(outfile, 'w')
f.write('\n'.join(lines))
f.close()

print('Done')