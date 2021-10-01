import pandas as pd
import numpy as np
import os
from subprocess import Popen

print('Reading Files')

tour = {}
tour[2015] = pd.read_csv(r'D:\TIM3.1\000000\scenario\Output\_tour_2.dat', '\t').query('pdpurp == 1')
tour[2040] = pd.read_csv(r'B:\model_development\TIM_3.1_2040\scenario\Output\_tour_2.dat', '\t').query('pdpurp == 1')
maz2at = pd.read_csv(r'D:\ref\maz2at.csv', index_col = 0)

outfile = r'D:\TIM3\TourModeShareByOriginAreaType_RAW.xlsx'
writer = pd.ExcelWriter(outfile)

print('Processing and Writing')

for year in tour:
    tour[year]['oat'] = tour[year]['topcl'].map(maz2at[str(year)])
    mode_trips_by_oat = tour[year][['oat', 'tmodetp', 'toexpfac']].groupby(['oat', 'tmodetp']).sum()['toexpfac'].reset_index().pivot('tmodetp', 'oat', 'toexpfac')
    mode_trips_by_oat.to_excel(writer, str(year))

writer.close()
Popen(outfile, shell = True)