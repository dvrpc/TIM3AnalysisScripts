import pandas as pd
import numpy as np
from subprocess import Popen

print('Reading')
fp = r'D:\TIM3.1\EITruckCalibrationNovember2020\scenario\Output\_trip_2.dat'
trip = pd.read_csv(fp, '\t')
veh_map = {1: 0, 2: 0, 3: 1, 4: 0.5, 5: 0.3, 6: 1, 8: 0, 9: 0, 10: 0}
per_map = {1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 1, 8: 0, 9: 0, 10: 0}

print('Arithmetic')
trip['veh'] = trip['trexpfac'] * (trip['mode'].map(veh_map))
trip['per'] = trip['trexpfac'] * (trip['mode'].map(per_map))

o_by_taz = trip[['otaz', 'veh', 'per']].groupby('otaz').sum()
d_by_taz = trip[['dtaz', 'veh', 'per']].groupby('dtaz').sum()

print('Writing')
outfile = r'D:\TIM3\TripEndsByTAZ.csv'
(o_by_taz + d_by_taz).to_csv(outfile)
Popen(outfile, shell = True)