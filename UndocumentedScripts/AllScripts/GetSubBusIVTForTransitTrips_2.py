import pandas as pd
import numpy as np
import os
from Util import WriteToTrace
             
trip_files = {3: r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\SA_MAZ-SA-v3_WalkWt10_DaySim1208_TransferWt0\_trip_2.dat',
              4: r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\SA_MAZ-SA-v3_WalkWt10_DaySim1208_SAWalkWt10\_trip_2.dat',
              5: r'T:\TIM_3.1\DVRPC_ABM_Testing\Scenario\Output\_trip_2.dat'}
skim_loc = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario'
outfiles = {3: r'D:\TIM3\TransitTripsWithSubBusIVT_WalkWt10_DaySim1208_No3.csv',
            4: r'D:\TIM3\TransitTripsWithSubBusIVT_WalkWt10_DaySim1208_No4.csv',
            5: r'D:\TIM3\TransitTripsWithSubBusIVT_WalkWt10_DaySim1208_No5.csv'}

sa2mode_file = r'D:\ref\sa2mode_w_stops.csv'
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

def read_skim(df, newcol, skim_path):

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

    df[newcol] = df['od'].map(vals)

    return vals

skim_paths = {'0000': {'bus': os.path.join(skim_loc, 'PuTSkim_0.00-6.00.IVTT(Bus)'),
                       'sub': os.path.join(skim_loc, 'PuTSkim_0.00-6.00.IVTT(Sub)')},
              '0600': {'bus': os.path.join(skim_loc, 'PuTSkim_6.00-10.00.IVTT(Bus)'),
                       'sub': os.path.join(skim_loc, 'PuTSkim_6.00-10.00.IVTT(Sub)')},
              '1000': {'bus': os.path.join(skim_loc, 'PuTSkim_10.00-15.00.IVTT(Bus)'),
                       'sub': os.path.join(skim_loc, 'PuTSkim_10.00-15.00.IVTT(Sub)')},
              '1500': {'bus': os.path.join(skim_loc, 'PuTSkim_15.00-19.00.IVTT(Bus)'),
                       'sub': os.path.join(skim_loc, 'PuTSkim_15.00-19.00.IVTT(Sub)')},
              '1900': {'bus': os.path.join(skim_loc, 'PuTSkim_19.00-0.00.IVTT(Bus)'),
                       'sub': os.path.join(skim_loc, 'PuTSkim_19.00-0.00.IVTT(Sub)')}
              }

#skims = {}
#for tod in skim_paths:
#    skims[tod] = {}
#    for mode in skim_paths[tod]:
#        WriteToTrace(Visum, 'Reading ' + skim_paths[tod][mode])
#        skims[tod][mode] = read_skim(skim_paths[tod][mode])

for i in range(3, 6):
    WriteToTrace(Visum, 'Reading Trip File %d'%(i))
    trip = pd.read_csv(trip_files[i], '\t').query('mode == 6')# and deptm >= 360 and deptm < 600')

    WriteToTrace(Visum, 'Classifying Travel Times')
    trip['tod'] = trip['deptm'].apply(classify_tod)
    tod_dummies = pd.get_dummies(trip['tod'])
    trip[tod_dummies.columns] = tod_dummies
    del tod_dummies

    WriteToTrace(Visum, 'Getting stop area modes')

    trip['omode'] = trip['otaz'].map(sa2mode['MODE'])
    trip['dmode'] = trip['dtaz'].map(sa2mode['MODE'])
    trip['osubinstop'] = trip['otaz'].map(sa2mode['SUBINSTOP']).astype(bool)
    trip['dsubinstop'] = trip['dtaz'].map(sa2mode['SUBINSTOP']).astype(bool)

    trip['osub'] = (trip['omode'] == 'Sub')
    trip['dsub'] = (trip['dmode'] == 'Sub')
    trip['obus'] = (trip['omode'] == 'Bus')
    trip['dbus'] = (trip['dmode'] == 'Bus')

    trip['obus_w_subinstop'] = (trip['obus'] & trip['osubinstop'])
    trip['dbus_w_subinstop'] = (trip['dbus'] & trip['dsubinstop'])
    trip['obus_wo_subinstop'] = (trip['obus'] & ~trip['osubinstop'])
    trip['dbus_wo_subinstop'] = (trip['dbus'] & ~trip['dsubinstop'])

    trip['odsub'] = (trip['osub'] & trip['dsub'])
    trip['odbus_w_subinstop'] = (trip['obus_w_subinstop'] & trip['dbus_w_subinstop'])
    trip['odbus_wo_subinstop'] = (trip['obus_wo_subinstop'] & trip['dbus_wo_subinstop'])


    WriteToTrace(Visum, 'Getting IVT For each trip')
    trip['od'] = list(zip(trip['otaz'], trip['dtaz']))
    for tod in skim_paths:
        for mode in skim_paths[tod]:
            WriteToTrace(Visum, 'Reading ' + skim_paths[tod][mode])
            read_skim(trip, 'ivt' + tod + mode, skim_paths[tod][mode])
            #trip['ivt' + tod + mode] = trip['od'].map(skims[tod][mode])

    trip['subivt'] = np.zeros_like(trip.index)
    trip['busivt'] = np.zeros_like(trip.index)

    for tod in skim_paths:
        for mode in skim_paths[tod]:
            trip[mode + 'ivt'] += trip[tod] * trip['ivt' + tod + mode]

    WriteToTrace(Visum, 'Writing Output %d'%(i))
    trip.to_csv(outfiles[i])

WriteToTrace(Visum, 'Done')