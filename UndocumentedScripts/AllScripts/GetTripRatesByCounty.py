import pandas as pd
import numpy as np
from subprocess import Popen

print('Reading Files')

trip = {}
trip[2015] = pd.read_csv(r'D:\TIM3.1\000000\scenario\Output\_trip_2.dat', '\t')
trip[2040] = pd.read_csv(r'B:\model_development\TIM_3.1_2040\scenario\Output\_trip_2.dat', '\t')
taz2county = pd.read_csv(r'D:\ref\taz2county.csv', index_col = 0)['County']

print('Processing')

o_by_county = {}
d_by_county = {}
for year in [2015, 2040]:
    trip[year]['ocounty'] = trip[year]['otaz'].map(taz2county)
    trip[year]['dcounty'] = trip[year]['dtaz'].map(taz2county)
    o_by_county[year] = trip[year].groupby('ocounty').sum()['trexpfac']
    d_by_county[year] = trip[year].groupby('dcounty').sum()['trexpfac']

print('Writing')

outfile = r'D:\TIM3\TripRatesByCounty.xlsx'
outdata = pd.Panel({'Origins': pd.DataFrame({2015: o_by_county[2015], 2040: o_by_county[2040]}),
                    'Destinations': pd.DataFrame({2015: d_by_county[2015], 2040: d_by_county[2040]})})
outdata.to_excel(outfile)
Popen(outfile, shell = True)

print('Go')