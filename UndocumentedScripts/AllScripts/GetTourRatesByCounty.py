import pandas as pd
import numpy as np
from subprocess import Popen

print('Reading Files')

tour = {}
tour[2015] = pd.read_csv(r'D:\TIM3.1\000000\scenario\Output\_tour_2.dat', '\t')
tour[2040] = pd.read_csv(r'B:\model_development\TIM_3.1_2040\scenario\Output\_tour_2.dat', '\t')
taz2county = pd.read_csv(r'D:\ref\taz2county.csv', index_col = 0)['County']

print('Processing')

to_by_county = {}
td_by_county = {}
for year in [2015, 2040]:
    tour[year]['tocounty'] = tour[year]['totaz'].map(taz2county)
    tour[year]['tdcounty'] = tour[year]['tdtaz'].map(taz2county)
    to_by_county[year] = tour[year].groupby('tocounty').sum()['toexpfac']
    td_by_county[year] = tour[year].groupby('tdcounty').sum()['toexpfac']

print('Writing')

outfile = r'D:\TIM3\TourRatesByCounty.xlsx'
outdata = pd.Panel({'Origins': pd.DataFrame({2015: to_by_county[2015], 2040: to_by_county[2040]}),
                    'Destinations': pd.DataFrame({2015: td_by_county[2015], 2040: td_by_county[2040]})})
outdata.to_excel(outfile)
Popen(outfile, shell = True)

print('Go')