from __future__ import division

import pandas as pd
import numpy as np
import os

base_path = r'D:\TIM3.1\CalibrationApril2021\scenario'
tour_file = os.path.join(base_path, 'Output', '_tour_2.dat')
trip_file = os.path.join(base_path, 'Output', '_trip_2.dat')
pnr_file = os.path.join(base_path, 'inputs', 'DVRPC_p_rNodes.dat')

mode_map = {1: 0, 2: 0, 3: 1, 4: 0.5, 5: 1/3, 6: 0, 7: 0, 8: 0, 9: 0} #5 should be 0.3 based on TIM3 inputs--DaySim has 1/3 hard-coded
times = range(1440)

def pivot(df, row, col, val):
    return df[[row, col, val]].groupby([row, col]).sum()[val].reset_index().pivot(row, col, val).fillna(0)

print('Reading')
pnr = pd.read_csv(pnr_file, '\t', index_col = 1)
tour = pd.read_csv(tour_file, '\t')
trip = pd.read_csv(trip_file, '\t')

print('Adding Fields')
tour['tourid'] = list(zip(tour['hhno'], tour['pno'], tour['day'], tour['tour']))
trip['veh_trips'] = (trip['trexpfac'] * (trip['mode'].map(mode_map)))
trip['olot'] = trip['otaz'].map(pnr['NodeID'])
trip['dlot'] = trip['dtaz'].map(pnr['NodeID'])

tourtrip = tour.merge(trip, on = ['hhno', 'pno', 'day', 'tour'])

to_pnr = tourtrip.query('tmodetp == 7 and dpurp == 10 and half == 1').set_index('tourid')
half1 = tourtrip.query('tmodetp == 7 and opurp == 10 and half == 1').set_index('tourid')
half2 = tourtrip.query('tmodetp == 7 and opurp == 10 and half == 2').set_index('tourid')

tour = tour.query('tmodetp == 7')
tour['mode'] = tour['tourid'].map(to_pnr['mode']) #Access mode (SOV, HOV2, or HOV3+)
tour['lot'] = tour['tourid'].map(half1['olot']).astype(int) #DaySim PnR Node ID
tour['arr'] = tour['tourid'].map(half1['deptm']).astype(int) #Arrival time at PnR Lot
tour['dep'] = tour['tourid'].map(half2['deptm']).astype(int) #Departure time from PnR Lot
tour['vehs'] = (tour['mode'].map(mode_map) * tour['toexpfac']) #Adjust for mode and expansion factor

print('Adding Up Loads')
c = 0
loads = pd.DataFrame(np.zeros((180, 1440)), index = range(1, 181), columns = range(1, 1441))
for i in tour.index:
    #for t in range(tour.loc[i, 'arr'], tour.loc[i, 'dep']):
    #    loads.iloc[tour.loc[i, 'lot'], t] += tour.loc[i, 'vehs']

    loads.loc[tour.loc[i, 'lot'], tour.loc[i, 'arr']:(tour.loc[i, 'dep']-1)] += tour.loc[i, 'vehs']
    c += 1
    if c % 1000 == 0:
        print(c)

loads.to_csv(r'D:\TIM3\PnRLoadReplication0423.csv')

print('Go')