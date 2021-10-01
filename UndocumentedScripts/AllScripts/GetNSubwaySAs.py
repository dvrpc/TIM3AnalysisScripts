import pandas as pd
import numpy as np

trip_file = r'B:\model_development\TIM_3.1\scenario\Output\SA_NoWalkSA\_trip_2.dat'
trip = pd.read_csv(trip_file, '\t').query('mode == 6')


sa2mode_file = r'D:\TIM3\sa2mode.csv'
sa2mode = pd.read_csv(sa2mode_file, index_col = 0)['MODE']

trip['omode'] = trip['otaz'].map(sa2mode)
trip['dmode'] = trip['dtaz'].map(sa2mode)

trip['osub'] = (trip['omode'] == 'Sub')
trip['dsub'] = (trip['dmode'] == 'Sub')
trip['odsub'] = (trip['osub'] & trip['dsub'])
trip['odnotsub'] = ~(trip['osub'] | trip['dsub'])

print('Including PnR')
print('=============')
print('Subway Chosen at Origin:      {}'.format((trip['osub']*trip['trexpfac']).sum()))
print('Subway Chosen at Destination: {}'.format((trip['dsub']*trip['trexpfac']).sum()))
print('Subway Chosen at Both:        {}'.format((trip['odsub']*trip['trexpfac']).sum()))
print('Subway Chosen at Neither:     {}'.format((trip['odnotsub']*trip['trexpfac']).sum()))

non_pnr = trip.query('opurp != 10 and dpurp != 10')

print('\n')
print('Excluding PnR')
print('=============')
print('Subway Chosen at Origin:      {}'.format((non_pnr['osub']*non_pnr['trexpfac']).sum()))
print('Subway Chosen at Destination: {}'.format((non_pnr['dsub']*non_pnr['trexpfac']).sum()))
print('Subway Chosen at Both:        {}'.format((non_pnr['odsub']*non_pnr['trexpfac']).sum()))
print('Subway Chosen at Neither:     {}'.format((non_pnr['odnotsub']*non_pnr['trexpfac']).sum()))