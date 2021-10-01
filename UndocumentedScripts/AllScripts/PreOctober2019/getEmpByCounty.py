import os
from subprocess import Popen

wd = os.getcwd()
per_file = os.path.join(wd, '_person_2.dat')
taz2cnty_file = os.path.join(wd, 'taz2county.csv')
outfile = os.path.join(wd, 'EmpByCounty.csv')

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
counties.sort()

emp_by_county = {}
for county in counties:
    emp_by_county[county] = 0

per = open(per_file, 'r')
first_line = True
i = 0
for line in per:
    entry = line.replace('\n', '').split('\t')
    if first_line:
        pwtaz = entry.index('pwtaz')
        psexpfac = entry.index('psexpfac')
        first_line = False
    else:
        if entry[pwtaz] == '-1': #Not a worker, so ignore
            continue
        pwcounty = taz2cnty[entry[pwtaz]]
        if not int(pwcounty[-1]) % 2:
            pwcounty = list(pwcounty)
            pwcounty[-1] = str(int(pwcounty[-1]) - 1)
            pwcounty = ''.join(pwcounty)
        emp_by_county[pwcounty] += float(entry[psexpfac])

lines = ['COUNTY,JOBS']
for county in counties:
    if int(county[-1])%2:
        lines.append('{0},{1}'.format(county, emp_by_county[county]))
        print '{0}: {1}'.format(county, emp_by_county[county])

with open(outfile, 'w') as f:
    f.write('\n'.join(lines))
    f.close()

Popen(outfile, shell = True)
