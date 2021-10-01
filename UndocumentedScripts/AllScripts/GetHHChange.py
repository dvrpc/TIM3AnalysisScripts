import pandas as pd
import numpy as np
from subprocess import Popen

infile_2015 = r'C:\Users\jflood\Documents\TIM31_Validation\scenario\inputs\_DVRPC_hrec.dat'
infile_2040 = r'C:\Users\jflood\Documents\TIM31_2040\scenario\inputs\_DVRPC_hrec.dat'

taz2county_file = r'C:\Migrate\ref\taz2fips.csv'
taz2county = pd.read_csv(taz2county_file, index_col = 0)['STATE_COUNTY_ID']

data = {}
data[2015] = pd.read_csv(infile_2015)
data[2040] = pd.read_csv(infile_2040)

data[2015]['hcounty'] = data[2015]['hhtaz'].map(taz2county)
data[2040]['hcounty'] = data[2040]['hhtaz'].map(taz2county)

counties = data[2015]['hcounty'].value_counts().index
outdata = pd.DataFrame(np.zeros((len(counties), 2)), index = counties, columns = [2015, 2040])

for year in [2015, 2040]:
    outdata[year] = data[year].groupby('hcounty').sum()['hhexpfac']

outfile = r'C:\Migrate\TIM3\HHChange1540.csv'
outdata.sort_index().to_csv(outfile)
Popen(outfile, shell = True)