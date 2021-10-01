import numpy as np
import pandas as pd
import csv
import os

def classify_time(time):
    if int(time) < 6*60:
        return '0000'
    elif int(time) < 10*60:
        return '0600'
    elif int(time) < 15*60:
        return '1000'
    elif int(time) < 19*60:
        return '1500'
    else:
        return '1900'

trip_file = r'D:\TIM3.1\200212_FullRunLessSASkimming\DVRPC_ABM\scenario\Output\_trip_2.dat'

Visum.Log(20480, 'Reading Trip Data')
auto_modes = [3, 4, 5]
trip_data = pd.read_csv(trip_file, '\t').query('mode in @auto_modes')

trip_data['tod'] = trip_data['deptm'].apply(classify_time)

N = trip_data.shape[0]

Visum.Log(20480, 'Reading Skims')
zones = np.array(Visum.Net.Zones.GetMultipleAttributes(['No']))[:, 0].astype(int)
dis = {'0000': pd.DataFrame(np.array(Visum.Net.Matrices.ItemByKey(401).GetValuesFloat()), zones, zones),
       '0600': pd.DataFrame(np.array(Visum.Net.Matrices.ItemByKey(402).GetValuesFloat()), zones, zones),
       '1000': pd.DataFrame(np.array(Visum.Net.Matrices.ItemByKey(403).GetValuesFloat()), zones, zones),
       '1500': pd.DataFrame(np.array(Visum.Net.Matrices.ItemByKey(404).GetValuesFloat()), zones, zones),
       '1900': pd.DataFrame(np.array(Visum.Net.Matrices.ItemByKey(405).GetValuesFloat()), zones, zones)}

def get_skim_dist(args):
    '''
    args: (tod, otaz, dtaz)
    '''
    global dis
    return dis[args[0]].loc[args[1], args[2]]

Visum.Log(20480, 'Comparing Distances')
trip_data['args'] = list(zip(trip_data['tod'], trip_data['otaz'], trip_data['dtaz']))
trip_data['skimdist'] = trip_data['args'].apply(get_skim_dist)
trip_data['distdiff'] = trip_data['skimdist'] - trip_data['travdist']

Visum.Log(20480, 'Writing Output')
outfile = r'D:\TIM3.1\200212_FullRunLessSASkimming\DVRPC_ABM\AutoTripDists.csv'
trip_data[['mode', 'opcl', 'dpcl', 'otaz', 'dtaz', 'tod', 'travdist', 'skimdist', 'distdiff', 'trexpfac']].to_csv(outfile)

Visum.Log(20480, 'Done')