import pandas as pd
import numpy as np
import os
from Util import WriteToTrace
             
trip_file = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\SA_MAZ-SA-v3_WalkWt10_DaySim1208\_trip_2.dat'
skim_loc = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario'
sa2mode_file = r'D:\sa2mode_w_stops.csv'
sa2mode = pd.read_csv(sa2mode_file, index_col = 0)

WriteToTrace(Visum, 'Reading maz2sa file')
maz2sa_file = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\microzonetostopareadistance.dat'
maz2sa = pd.read_csv(maz2sa_file, ' ')

WriteToTrace(Visum, 'Identifying subway-accessible MAZs')
maz2sa['mode'] = maz2sa['stopareaid'].map(sa2mode['MODE'])
maz2sub = maz2sa[maz2sa['mode'] == 'Sub'].query('distance <= 2640')
subway_mazs = list(set(maz2sub['zoneid']))

def classify_tod(t):
    if t < 360:
        return '0000'
    elif t < 600:
        return '0600'
    elif t < 900:
        return '1000'
    elif t < 1140:
        return '1500'
    else:
        return '1900'

StopAreas = np.array(Visum.Net.StopAreas.GetMultiAttValues("No"))[:,1].astype(int)

def read_skim(skim_path):

    global StopAreas

    try:
        Visum.Net.AddMatrix(10000, objectTypeRef=4, MatrixType=4)
    except Exception:
        pass

    mat = Visum.Net.Matrices.ItemByKey(10000)
    mat.Init()
    mat.Open(skim_path, ReadAdditive = True)
    vals = pd.DataFrame(np.array(mat.GetValuesFloat()), index = StopAreas, columns = StopAreas)

    WriteToTrace(Visum, 'Formatting Skim Data')
    vals = pd.melt(vals.reset_index(), id_vars = ['index'], value_vars = list(StopAreas))
    vals['od'] = list(zip(vals['index'], vals['variable']))
    vals = vals.set_index('od')['value']

    return vals

skim_paths = {#'0000': {'bus': os.path.join(skim_loc, 'PuTSkim_0.00-6.00.IVTT(Bus)'),
              #         'sub': os.path.join(skim_loc, 'PuTSkim_0.00-6.00.IVTT(Sub)')},
              '0600': {'bus': os.path.join(skim_loc, 'PuTSkim_6.00-10.00.IVTT(Bus)'),
                       'sub': os.path.join(skim_loc, 'PuTSkim_6.00-10.00.IVTT(Sub)')},
              #'1000': {'bus': os.path.join(skim_loc, 'PuTSkim_10.00-15.00.IVTT(Bus)'),
              #         'sub': os.path.join(skim_loc, 'PuTSkim_10.00-15.00.IVTT(Sub)')},
              #'1500': {'bus': os.path.join(skim_loc, 'PuTSkim_15.00-19.00.IVTT(Bus)'),
              #         'sub': os.path.join(skim_loc, 'PuTSkim_15.00-19.00.IVTT(Sub)')},
              #'1900': {'bus': os.path.join(skim_loc, 'PuTSkim_19.00-0.00.IVTT(Bus)'),
              #         'sub': os.path.join(skim_loc, 'PuTSkim_19.00-0.00.IVTT(Sub)')}
              }

skims = {}
for tod in skim_paths:
    skims[tod] = {}
    for mode in skim_paths[tod]:
        WriteToTrace(Visum, 'Reading ' + skim_paths[tod][mode])
        skims[tod][mode] = read_skim(skim_paths[tod][mode])

WriteToTrace(Visum, 'Reading Trip File')
trip = pd.read_csv(trip_file, '\t').query('mode == 6 and deptm >= 360 and deptm < 600')

WriteToTrace(Visum, 'Classifying Travel Times')
trip['tod'] = trip['deptm'].apply(classify_tod)
tod_dummies = pd.get_dummies(trip['tod'])
trip[tod_dummies.columns] = tod_dummies
del tod_dummies

WriteToTrace(Visum, 'Getting IVT For each trip')
trip['od'] = list(zip(trip['otaz'], trip['dtaz']))
for tod in skims:
    for mode in skims[tod]:
        trip['ivt' + tod + mode] = trip['od'].map(skims[tod][mode])

trip['subivt'] = np.zeros_like(trip.index)
trip['busivt'] = np.zeros_like(trip.index)

for tod in skims:
    for mode in skims[tod]:
        trip[mode + 'ivt'] += trip[tod] * trip['ivt' + tod + mode]

WriteToTrace(Visum, 'Getting stop area modes')
half = trip#.query('opcl in @subway_mazs and dpcl in @subway_mazs and travdist >= 2')
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

WriteToTrace(Visum, 'Writing Output')
trip.to_csv(r'D:\TIM3\AMTransitTripsWithSubBusIVT.csv')

WriteToTrace(Visum, 'Done')