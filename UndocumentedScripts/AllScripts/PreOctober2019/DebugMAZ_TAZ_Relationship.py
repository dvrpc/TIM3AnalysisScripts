import pandas as pd
import os

base_path = r'R:\Model_Development\TIM_3.1\scenario'
trip_file = os.path.join(base_path, 'Output', '_trip_2.dat')
hh_file = os.path.join(base_path, 'inputs', '_DVRPC_hrec.dat')
#hh_file = os.path.join(base_path, 'Output', '_household_2.dat')
maz2taz_file = os.path.join(base_path, 'maz2taz.csv')

maz2taz = pd.read_csv(maz2taz_file, index_col = 0)['TAZ_P']
hh = pd.read_csv(hh_file, delimiter = ',')
#trip = pd.read_csv(trip_file, delimiter = '\t')

hh['hhtaz2'] = hh['hhparcel'].map(maz2taz)
hh['taz_mismatch'] = hh['hhtaz'] != hh['hhtaz2']

print(hh[hh['taz_mismatch']==True]['hhexpfac'].sum())
print(hh[hh['taz_mismatch']==False]['hhexpfac'].sum())

#trip['otaz2'] = trip['opcl'].map(maz2taz)
#trip['dtaz2'] = trip['dpcl'].map(maz2taz)

#trip['otaz_mismatch'] = trip['otaz'] != trip['otaz2']
#trip['dtaz_mismatch'] = trip['dtaz'] != trip['dtaz2']

#print(trip['otaz_mismatch'].sum())
#print(trip['dtaz_mismatch'].sum())

print('Go')