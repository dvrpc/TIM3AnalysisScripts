import pandas as pd
import numpy as np
import os

trip_file = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\SA_MAZ-SA-v3_WalkWt10_DaySim1208\_trip_2.dat'
trip = pd.read_csv(trip_file, '\t').query('mode == 6')

def addup(df, var):
    return (df[var]*df['trexpfac']).sum()

sa2mode_file = r'D:\sa2mode_w_stops.csv'
sa2mode = pd.read_csv(sa2mode_file, index_col = 0)

print('Reading maz2sa file')
maz2sa_file = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\microzonetostopareadistance.dat'
maz2sa = pd.read_csv(maz2sa_file, ' ')

print('Identifying subway-accessible MAZs')
maz2sa['mode'] = maz2sa['stopareaid'].map(sa2mode['MODE'])
maz2sub = maz2sa[maz2sa['mode'] == 'Sub'].query('distance <= 2640')
subway_mazs = list(set(maz2sub['zoneid']))

half = trip.query('opcl in @subway_mazs and dpcl in @subway_mazs')
half['omode'] = half['otaz'].map(sa2mode['MODE'])
half['dmode'] = half['dtaz'].map(sa2mode['MODE'])
half['osubinstop'] = half['otaz'].map(sa2mode['SUBINSTOP']).astype(bool)
half['dsubinstop'] = half['dtaz'].map(sa2mode['SUBINSTOP']).astype(bool)

half['osub'] = (half['omode'] == 'Sub')
half['dsub'] = (half['dmode'] == 'Sub')
half['obus'] = (half['omode'] == 'Bus')
half['dbus'] = (half['dmode'] == 'Bus')

half['obus_w_subinstop'] = (half['obus'] & half['osubinstop'])
half['dbus_w_subinstop'] = (half['dbus'] & half['dsubinstop'])
half['obus_wo_subinstop'] = (half['obus'] & ~half['osubinstop'])
half['dbus_wo_subinstop'] = (half['dbus'] & ~half['dsubinstop'])

half['odsub'] = (half['osub'] & half['dsub'])
half['odbus_w_subinstop'] = (half['obus_w_subinstop'] & half['dbus_w_subinstop'])
half['odbus_wo_subinstop'] = (half['obus_wo_subinstop'] & half['dbus_wo_subinstop'])

results = {}
results['Total Trips'] = half['trexpfac'].sum()

results['Subway at Origin'] = addup(half, 'osub')
results['Bus w Subway at Origin'] = addup(half, 'obus_w_subinstop')
results['Bus wo Subway at Origin'] = addup(half, 'obus_wo_subinstop')

results['Subway at Destination'] = addup(half, 'dsub')
results['Bus w Subway at Destination'] = addup(half, 'dbus_w_subinstop')
results['Bus wo Subway at Destination'] = addup(half, 'dbus_wo_subinstop')

results['Subway at Both'] = addup(half, 'odsub')
results['Bus w Subway at Both'] = addup(half, 'odbus_w_subinstop')
results['Bus wo Subway at Both'] = addup(half, 'odbus_wo_subinstop')

pd.Series(results).to_csv(r'D:\TIM3\TransitChoiceWithSubAtStop.csv')

print('Go')