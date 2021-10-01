import pandas as pd
import numpy as np
import os

taz2side = {}
for i in range(18000):
    taz2side[i] = 1
for i in range(18000, 26000):
    taz2side[i] = 0
for i in range(50000, 53000):
    taz2side[i] = 1
for i in range(53000, 58000):
    taz2side[i] = 0
for i in range(58000, 59000):
    taz2side[i] = 1

tripfile = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\_trip_2.dat'
mfile = r'D:\TIM3\2159.csv'

print('Reading Trip File')
trip = pd.read_csv(tripfile, delimiter = '\t')
print('Reading Matrix')
m2159 = pd.read_csv(mfile, index_col = 0)

print('Unpivoting Matrix')
zones = m2159.index.values
N = len(zones)
ozones = np.repeat(zones, N)
dzones = np.hstack(N*[zones])
odpairs = list(zip(ozones, dzones))
m2159up = pd.Series(np.reshape(m2159.values, N**2), index = odpairs)

print('Identifying matrix 2159 values for each trip')
trip['odpair'] = list(zip(trip['otaz'], trip['dtaz']))
trip['matrix2159'] = trip['odpair'].map(m2159up)

#print('Getting Origin and Destination Purpose Tuples')
#trip['odpurp'] = list(zip(trip['opurp'], trip['dpurp']))


print('Identifying river crossing trips')
trip['oside'] = trip['otaz'].map(taz2side)
trip['dside'] = trip['dtaz'].map(taz2side)
trip['rx'] = trip['oside'] != trip['dside']
crossings = trip[trip['rx']]
work_crossings = crossings.query('opurp == 1 or dpurp == 1')
nonwork_crossings = crossings.query('opurp != 1 and dpurp != 1')

total_crossings = crossings['trexpfac'].sum()
reduced_crossings = (crossings['matrix2159']*crossings['trexpfac']).sum()
nonwork_crossings = work_crossings['trexpfac'].sum() + (nonwork_crossings['matrix2159']*nonwork_crossings['trexpfac']).sum()



print('Total River Crossings: %d'%(total_crossings))
print('Full Reduction:        %d'%(reduced_crossings))
print('Nonwork Reduction:     %d'%(nonwork_crossings))

print('Go')