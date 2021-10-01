from __future__ import division
import pandas as pd
import numpy as np
from numpy import inf

#trip_file = r'T:\TIM_3.1\191018_StraightLineDistAll\scenario\Output\_trip_2.dat'
#maz2sa_file = r'T:\TIM_3.1\191018_StraightLineDistAll\scenario\maz2sa_dist.dat'
trip_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\Output\_trip_2.dat'
maz2sa_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\microzonetostopareadistance.dat'

sa2mode_file = r'D:\TIM3\sa2mode.csv'

print('===READING FILES===')
print('Reading MAZ-SA distance file')
maz2sa = pd.read_csv(maz2sa_file, ' ')
print('Reading SA-Mode file')
sa2mode = pd.read_csv(sa2mode_file, index_col = 0)['MODE']
print('Reading Trip File')
trip = pd.read_csv(trip_file, '\t')
print('\n')

print('===Identifying MAZs that are accessible to subway stops===')
print('Identifying subway stops')
maz2sa['mode'] = maz2sa['stopareaid'].map(sa2mode)
print('Getting list of subway-accessible MAZs')
subway_mazs = list(set(maz2sa.query('mode == "Sub"')['zoneid']))
print('Filtering out non-subway-accessible MAZs')
sub2sub = trip[['opcl', 'dpcl', 'mode', 'travdist', 'trexpfac']].query('opcl in @subway_mazs and dpcl in @subway_mazs')
sub2sub_trips = sub2sub['trexpfac'].sum()

print('\n')
print('===Calculating Subway-Accessible Mode Share===')
print('Grouping trips by mode')
mode_trips = sub2sub[['mode', 'trexpfac']].groupby('mode').sum()['trexpfac'].sort_index()
print('Calculating mode share')
#mode_share = pd.Series((mode_trips / mode_trips.sum()), index = ['Walk', 'Bike', 'SOV', 'HOV2', 'HOV3+', 'Transit', 'School Bus', 'Other'])
#mode_share = {}
#mode_share['Bike'] = mode_trips[2] / sub2sub_trips
#mode_share['SOV'] = mode_trips[3] / sub2sub_trips
#mode_share['HOV2'] = mode_trips[4] / sub2sub_trips
#mode_share['HOV3+'] = mode_trips[5] / sub2sub_trips
#mode_share['Transit'] = mode_trips[6] / sub2sub_trips
#mode_share['School Bus'] = mode_trips[8] / sub2sub_trips
#mode_share['Other'] = mode_trips[9] / sub2sub_trips
#mode_share = pd.Series(mode_share)

#mode_trips.to_csv(r'D:\TIM3\Sub2SubModeTrips_2mi.csv')

modes = [1, 2, 3, 4, 5, 6, 8, 9]
bound_list = [(0, 0.5), (0.5, 1), (1, 1.5), (1.5, 2), (2, 3), (3, 5), (5, 10), (10, inf)]

M = len(modes)
N = len(bound_list)

output = pd.DataFrame(np.zeros((M, N)), index = modes, columns = [str(bounds[0]) + '-' + str(bounds[1]) + ' mi' for bounds in bound_list])

for bounds in bound_list:
    min_dist = bounds[0]
    max_dist = bounds[1]
    sub2sub_dist = sub2sub.query('travdist >= @min_dist and travdist < @max_dist')
    mode_trips = sub2sub_dist.groupby('mode').sum()['trexpfac']

    for mode in mode_trips.index:
        output.loc[mode, str(min_dist) + '-' + str(max_dist) + ' mi'] += mode_trips[mode]

output.to_csv(r'D:\TIM3\Sub2SubModeTrips_Acc_RAW_Testing.csv')  

print('\n')

#print(mode_share)

print('\n')
print(mode_trips)
print(sub2sub.shape[0])
print(sub2sub['trexpfac'].sum())

f = open(r'D:\TIM3\subway_mazs.txt', 'w')
f.write('\n'.join([str(mazid) for mazid in subway_mazs]))
f.close()