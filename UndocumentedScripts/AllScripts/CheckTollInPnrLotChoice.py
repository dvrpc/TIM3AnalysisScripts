import pandas as pd
import numpy as np
import os

#runs = ['00NoToll', '01Toll']
runs = ['0518']
base_path = r'D:\TIM3.1\TestPnRShadowPriceConvergence\scenario\Output'

def pivot(df, row, col, val):
    return df[[row, col, val]].groupby([row, col]).sum()[val].reset_index().pivot(row, col, val).fillna(0)

taz2fips_file = r'D:\ref\taz2state.csv'
taz2fips = pd.read_csv(taz2fips_file, index_col = 0)
taz2fips['state'] = taz2fips['STATEFP00'].astype(str)
#taz2fips['west'] = ((taz2fips['state'] == '42') | (taz2fips['state'] == '10') | (taz2fips['state'] == '24'))
#taz2fips['east'] = (taz2fips['state'] == '34')

taz2fips['side'] = np.where(taz2fips['state'] == '34', 'east', 'west')

output = {}
for run in runs:
    trip_file = os.path.join(base_path, '_trip_2.dat')
    trip = pd.read_csv(trip_file, '\t').query('opurp == 0 and dpurp == 10') #Auto leg of PnR trips
    trip['oside'] = trip['otaz'].map(taz2fips['side'])
    trip['dside'] = trip['dtaz'].map(taz2fips['side'])
    output[run] = pivot(trip, 'oside', 'dside', 'trexpfac')

print('Done')