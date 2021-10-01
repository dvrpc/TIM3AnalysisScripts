import pandas as pd
import os
from subprocess import Popen

fp = r'T:\TIM_3.1\200504_LowerOtherTours\scenario\Output\_tour_2.dat'
tour = pd.read_csv(fp, '\t').query('pdpurp == 7')

taz2county = pd.read_csv(r'D:\ref\taz2fips.csv', index_col = 0)['STATE_COUNTY_ID']

tour['tocounty'] = tour['totaz'].map(taz2county)
tour['tdcounty'] = tour['tdtaz'].map(taz2county)

tour_flow = tour[['tocounty', 'tdcounty', 'toexpfac']].groupby(['tocounty', 'tdcounty']).sum()['toexpfac'].reset_index().pivot('tocounty', 'tdcounty', 'toexpfac').fillna(0)

outfile = r'D:\TIM3\SocRecTourFlow6May.csv'
tour_flow.to_csv(outfile)
Popen(outfile, shell = True)