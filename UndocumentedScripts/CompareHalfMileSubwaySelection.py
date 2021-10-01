import pandas as pd
import numpy as np
from subprocess import Popen

print('Reading after file')
trip_file1 = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\_trip_2.dat'
trip1 = pd.read_csv(trip_file1, '\t').query('mode == 6')

print('Reading before file')
#trip_file0 = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\SA_MAZ-SA-v3_WalkWt10_DaySim1208\_trip_2.dat'
#trip0 = pd.read_csv(trip_file0, '\t').query('mode == 6')
trip0 = trip1.copy()

print('Reading sa2mode file')
sa2mode_file = r'D:\TIM3\sa2mode.csv'
sa2mode = pd.read_csv(sa2mode_file, index_col = 0)['MODE']

print('Reading maz2sa file')
maz2sa_file = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\microzonetostopareadistance.dat'
maz2sa = pd.read_csv(maz2sa_file, ' ')

print('Identifying subway-accessible MAZs')
maz2sa['mode'] = maz2sa['stopareaid'].map(sa2mode)
maz2sub = maz2sa[maz2sa['mode'] == 'Sub'].query('distance <= 2640')
subway_mazs = list(set(maz2sub['zoneid']))

print('Filtering trip files for subway accessibility')
#trip0 = trip0.query('opcl in @subway_mazs and dpcl in @subway_mazs')
trip1 = trip1.query('opcl in @subway_mazs and dpcl in @subway_mazs')

trip0['omode'] = trip0['otaz'].map(sa2mode)
trip0['dmode'] = trip0['dtaz'].map(sa2mode)
trip1['omode'] = trip1['otaz'].map(sa2mode)
trip1['dmode'] = trip1['dtaz'].map(sa2mode)

outdata = pd.DataFrame(np.zeros((5, 2)),
                       index = ['Total Trips', 'Subway at Origin', 'Subway at Destination', 'Subway at Both', 'Subway at Neither'],
                       columns = ['Total', 'Half Mile'])

outdata[outdata.columns[0]] = [trip0['trexpfac'].sum(),
                               ((trip0['omode'] == 'Sub')*trip0['trexpfac']).sum(),
                               ((trip0['dmode'] == 'Sub')*trip0['trexpfac']).sum(),
                               (((trip0['omode'] == 'Sub') & (trip0['dmode'] == 'Sub'))*trip0['trexpfac']).sum(),
                               (((trip0['omode'] != 'Sub') & (trip0['dmode'] != 'Sub'))*trip0['trexpfac']).sum()]

outdata[outdata.columns[1]] = [trip1['trexpfac'].sum(),
                               ((trip1['omode'] == 'Sub')*trip1['trexpfac']).sum(),
                               ((trip1['dmode'] == 'Sub')*trip1['trexpfac']).sum(),
                               (((trip1['omode'] == 'Sub') & (trip1['dmode'] == 'Sub'))*trip1['trexpfac']).sum(),
                               (((trip1['omode'] != 'Sub') & (trip1['dmode'] != 'Sub'))*trip1['trexpfac']).sum()]

outfile = r'D:\TIM3\TotalVHalfMile_Wkt25.csv'
outdata.T.to_csv(outfile)
Popen(outfile, shell = True)

print('Go')