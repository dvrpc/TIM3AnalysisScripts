import pandas as pd
import numpy as np
import os

base_path = r'D:\TIM3.1\CalibrationApril2021\scenario'
trip_file = os.path.join(base_path, 'Output', '_trip_2.dat')
pnr_file = os.path.join(base_path, 'inputs', 'DVRPC_p_rNodes.dat')

mode_map = {1: 0, 2: 0, 3: 1, 4: 0.5, 5: 0.3, 6: 0, 7: 0, 8: 0, 9: 0}
times = range(1440)

def pivot(df, row, col, val):
    return df[[row, col, val]].groupby([row, col]).sum()[val].reset_index().pivot(row, col, val).fillna(0)

print('Reading')
pnr = pd.read_csv(pnr_file, '\t', index_col = 1)
trip = pd.read_csv(trip_file, '\t')
trip['veh_trips'] = (trip['trexpfac'] * (trip['mode'].map(mode_map)))

print('Filtering for PnR trips')
to_pnr = trip.query('opurp == 0 and dpurp == 10')
from_pnr = trip.query('opurp == 10 and dpurp == 0')

print('Adding PnR Node ID')
to_pnr['pnr_node'] = to_pnr['dtaz'].map(pnr['NodeID'])
from_pnr['pnr_node'] = from_pnr['otaz'].map(pnr['NodeID'])

print('Grouping By Entries and Exits')
entries = pivot(to_pnr, 'pnr_node', 'arrtm', 'veh_trips')
exits = pivot(from_pnr, 'pnr_node', 'deptm', 'veh_trips')

print('Obtaining PnR Loads')
pnr_loads = pd.DataFrame(np.zeros((180, 1440)), range(1, 181), times)
try:
    times[0] = entries[0]
except KeyError:
    pass
for t in times[1:]:
    try:
        pnr_loads[t] = pnr_loads[t-1] + entries[t]
    except KeyError:
        pnr_loads[t] = pnr_loads[t-1]
    try:
        pnr_loads[t] = np.maximum(pnr_loads[t] - exits[t], 0)
    except KeyError:
        pass

pnr_loads.to_csv(r'D:\TIM3\PnR_Loads.csv')

print('Go')