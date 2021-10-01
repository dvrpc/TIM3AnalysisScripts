import pandas as pd
import numpy as np

mode_map = {1: 0, 2: 0, 3: 1, 4: 0.5, 5: 0.3, 6: 0, 7: 0, 8: 0, 9: 0}

def classify_time(args):
    deptm = args[0]
    arrtm = args[1]
    half = args[2]
    if half == 1:
        return arrtm
    else:
        return deptm

print('Reading OD Pairs')
od_file = r'D:\TIM3\BetsyRossWBOD.csv'
od = pd.read_csv(od_file)
od_pairs = list(zip(od['O'], od['D']))
o = od['O'].values
d = od['D'].values

print('Reading Tour File')
tour_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\Output\_tour_2.dat'
tour = pd.read_csv(tour_file, '\t')

print('Reading Trip File')
trip_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\Output\_trip_2.dat'
trip = pd.read_csv(trip_file, '\t')

print('Merging Files')
tourtrip = tour.merge(trip, on = ['hhno', 'pno', 'day', 'tour'])
tourtrip['od'] = list(zip(tourtrip['otaz'], tourtrip['dtaz']))

print('Classifying Time')
tourtrip['args'] = list(zip(tourtrip['deptm'], tourtrip['arrtm'], tourtrip['half']))
tourtrip['time'] = tourtrip['args'].apply(classify_time)

print('Identifying Betsy Ross Trips')
#tourtrip['to_br'] = tourtrip['od'].apply(lambda x: x in od_pairs)
to_br = tourtrip.query('otaz in @o and dtaz in @d and time >= 360 and time < 600')
to_br['veh_trips'] = to_br['mode'].map(mode_map)*to_br['trexpfac']

print(to_br[['pdpurp', 'veh_trips']].groupby('pdpurp').sum()['veh_trips'])

print('Go')