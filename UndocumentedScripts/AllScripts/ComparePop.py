import pandas as pd
import numpy as np
import os
from subprocess import Popen

print('Reading')
#old_hh = pd.read_csv(r'T:\TIM_3.1\TIM31_Testing\scenario\Output\_household_2.dat', '\t')
#old_per = pd.read_csv(r'T:\TIM_3.1\TIM31_Testing\scenario\Output\_person_2.dat', '\t')
#new_hh = pd.read_csv(r'D:\TIM3.1\000000\scenario\Output\_household_2.dat', '\t')
#new_per = pd.read_csv(r'D:\TIM3.1\000000\scenario\Output\_person_2.dat', '\t')
old_hh = pd.read_csv(r'T:\TIM_3.1\TIM31_Testing\scenario\inputs\_DVRPC_hrec.dat', ',')
old_per = pd.read_csv(r'T:\TIM_3.1\TIM31_Testing\scenario\inputs\_DVRPC_prec.dat', ',')
new_hh = pd.read_csv(r'D:\TIM3.1\000000\scenario\inputs\_DVRPC_hrec.dat', ',')
new_per = pd.read_csv(r'D:\TIM3.1\000000\scenario\inputs\_DVRPC_prec.dat', ',')
taz2county = pd.read_csv(r'D:\ref\taz2fips.csv', index_col = 0)['STATE_COUNTY_ID']

print('Processing')
old = old_hh.merge(old_per, on = 'hhno')
new = new_hh.merge(new_per, on = 'hhno')
old['hhcounty'] = old['hhtaz'].map(taz2county)
new['hhcounty'] = new['hhtaz'].map(taz2county)
old_by_hh = old.groupby('hhcounty').sum()['psexpfac']
new_by_hh = new.groupby('hhcounty').sum()['psexpfac']
popchange = pd.DataFrame({'Old': old_by_hh, 'New': new_by_hh})

print('Writing')
outfile = r'D:\TIM3\PopChangeByCountyPS.csv'
popchange.to_csv(outfile)
Popen(outfile, shell = True)