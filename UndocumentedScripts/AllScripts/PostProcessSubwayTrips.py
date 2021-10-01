import pandas as pd
import numpy as np
import os

infile = r'D:\TIM3\TransitTripsWithSubBusIVT_WalkWt10_DaySim1208_TransferWt0.csv'
outfile = infile.replace('.csv', '_HalfMile.csv')

sa2mode_file = r'D:\ref\sa2mode_w_stops.csv'
sa2mode = pd.read_csv(sa2mode_file, index_col = 0)

print('Reading maz2sa file')
maz2sa_file = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\microzonetostopareadistance.dat'
maz2sa = pd.read_csv(maz2sa_file, ' ')

print('Identifying subway-accessible MAZs')
maz2sa['mode'] = maz2sa['stopareaid'].map(sa2mode['MODE'])
maz2sub = maz2sa[maz2sa['mode'] == 'Sub'].query('distance <= 2640')
subway_mazs = list(set(maz2sub['zoneid']))

print('Reading in trip file')
trip = pd.read_csv(infile)

print('Filtering Trips')
trip = trip.query('opcl in @subway_mazs and dpcl in @subway_mazs and travdist >= 2')

print('Writing out trip file')
trip.to_csv(outfile, index = False)

print('Done')