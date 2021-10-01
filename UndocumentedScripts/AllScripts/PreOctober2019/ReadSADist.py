import pandas as pd
import os

print('Reading Trip File')
infile = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\0829_SA\_trip_2.dat'
data = pd.read_csv(infile, sep = '\t').query('mode == 6')

print('Reading maz to sa file')
maz2sa_file = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\microzonetostopareadistance.dat'
maz2sa = pd.read_csv(maz2sa_file, sep = ' ')

print('Getting access and egress distances')
maz2sa['maz2sa'] = list(zip(maz2sa['zoneid'], maz2sa['stopareaid']))
maz2sa = maz2sa.set_index('maz2sa')

data['omaz2sa'] = list(zip(data['opcl'], data['otaz']))
data['dmaz2sa'] = list(zip(data['dpcl'], data['dtaz']))

data['access_dist'] = data['omaz2sa'].map(maz2sa['distance'])
data['egress_dist'] = data['dmaz2sa'].map(maz2sa['distance'])

print('Writing outfile')
data[['hhno', 'pno', 'day', 'tour', 'half', 'tseg', 'opcl', 'otaz', 'access_dist', 'dpcl', 'dtaz', 'egress_dist']].to_csv(r'D:\TIM3\MAZ_SA_Choices.csv')

print('Go')