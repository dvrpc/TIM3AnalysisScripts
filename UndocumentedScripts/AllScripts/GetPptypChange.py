import pandas as pd
import numpy as np
import os
from subprocess import Popen

hh2015_file = r'C:\Users\jflood\Documents\TIM31_Validation\scenario\inputs\_DVRPC_hrec.dat'
ps2015_file = r'C:\Users\jflood\Documents\TIM31_Validation\scenario\inputs\_DVRPC_prec.dat'
hh2040_file = r'C:\Users\jflood\Documents\TIM31_2040\scenario\inputs\_DVRPC_hrec.dat'
ps2040_file = r'C:\Users\jflood\Documents\TIM31_2040\scenario\inputs\_DVRPC_prec.dat'
taz2county_file = r'C:\Migrate\ref\taz2fips.csv'

taz2county = pd.read_csv(taz2county_file, index_col = 0)['STATE_COUNTY_ID']

hh2015 = pd.read_csv(hh2015_file, ',')
ps2015 = pd.read_csv(ps2015_file, ',')
hh2040 = pd.read_csv(hh2040_file, ',')
ps2040 = pd.read_csv(ps2040_file, ',')

hhper = {}
hhper[2015] = hh2015.merge(ps2015, on = 'hhno')
hhper[2040] = hh2040.merge(ps2040, on = 'hhno')

counties = taz2county.value_counts().index
for year in [2015, 2040]:
    hhper[year]['hcounty'] = hhper[year]['hhtaz'].map(taz2county)

pptyps = hhper[2015]['pptyp'].value_counts().sort_index().index

#for county in counties:
#    print(county)
#    outdata = pd.DataFrame(np.zeros((len(pptyps), len(hhper))), index = pptyps, columns = [2015, 2040])
#    for year in [2015, 2040]:
    
#        outdata[year] = hhper[year].query('hcounty == @county').groupby('pptyp').sum()['psexpfac']

#    outfile = r'D:\TIM3\pptypChange{}.csv'.format(county)
#    outdata.to_csv(outfile)
#    #Popen(outfile, shell = True)

outdata = pd.DataFrame(np.zeros((len(counties), 2)), index = counties, columns = [2015, 2040])
for year in [2015, 2040]:
    outdata[year] = hhper[year].groupby('hcounty').sum()['psexpfac']

outfile = r'C:\Migrate\TIM3\PopChangeByCounty1540NewPopSim.csv'
outdata.sort_index().to_csv(outfile)
Popen(outfile, shell = True)