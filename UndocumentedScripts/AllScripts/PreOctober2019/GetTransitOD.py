import pandas as pd
import numpy as np
import os

#base_path = r'T:\TIM_3.1\190802_FullTest\scenario'
#base_path = r'R:\Model_Development\TIM_3.1\scenario'
base_path = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario'
trip_file = os.path.join(base_path, 'Output', '0829_SA', '_trip_2.dat')
maz2sa_file = os.path.join(base_path, 'microzonetostopareadistance.dat')
sa2mode_file = r'D:\TIM3\StopArea2Mode.csv'
taz2county_file = r'D:\TIM3\taz2county.csv'
outfile = os.path.join(base_path, 'DSTrTripsByAvailModeCounty.csv')
outfile_sub = outfile.replace('.csv', '_SUB.csv')

print('Reading files')
trip = pd.read_csv(trip_file, delimiter = '\t')
print('Trip file read')
sa2mode = pd.read_csv(sa2mode_file, index_col = 0)['MODE']
print('SA-Mode file read')
maz2sa = pd.read_csv(maz2sa_file, delimiter = ' ')
print('MAZ-SA file read')
taz2county = pd.read_csv(taz2county_file, index_col = 0)['County']
print('TAZ-County file read')

print('Filtering out non-transit trips')
trip = trip[['hhno', 'pno', 'tour', 'half', 'tseg', 'mode', 'pathtype', 'deptm', 'otaz', 'opcl', 'dtaz', 'dpcl', 'travdist', 'travtime', 'travcost', 'trexpfac']].query('mode == 6')

print('Adding mode to MAZ-Stop Area correspondance')
maz2sa['mode'] = maz2sa['stopareaid'].map(sa2mode)

print('Creating dictionary of available travel modes for each MAZ')
gb_maz = maz2sa.groupby('zoneid')
maz_modes = gb_maz['mode'].value_counts()
maz2modes = {}
for maz in gb_maz.sum().index:
    maz2modes[maz] = ','.join(list(maz_modes.loc[maz].index))

print('Adding available transit modes to trip file')
trip['otrmodes'] = trip['opcl'].map(maz2modes)
trip['dtrmodes'] = trip['dpcl'].map(maz2modes)

available_modes = list(sa2mode.value_counts().index)
for mode in available_modes:
    print('Adding trip fields indicating whether or not ' + mode + ' is available')
    trip['o_' + mode] = trip['otrmodes'].fillna('').apply(lambda modes: mode in modes.split(',')).astype(int)
    trip['d_' + mode] = trip['dtrmodes'].fillna('').apply(lambda modes: mode in modes.split(',')).astype(int)

print('Adding origin and destination counties')
trip['ocounty'] = trip['otaz'].map(taz2county)
trip['dcounty'] = trip['dtaz'].map(taz2county)

print('Writing File')
cols = ['hhno', 'pno', 'tour', 'half', 'tseg', 'pathtype', 'deptm']
cols += ['ocounty', 'otaz', 'opcl', 'dcounty', 'dtaz', 'dpcl']
for mode in available_modes:
    cols += ['o_' + mode, 'd_' + mode]
cols += ['travdist', 'travtime', 'travcost', 'trexpfac']
trip[cols].to_csv(outfile)
trip[cols].query('o_Sub == 1 or d_Sub == 1').to_csv(outfile_sub)

print('File Written')