import os
from dsa_util import *
from subprocess import Popen

base_path = r'T:\TIM_3.1\200212_FullRunLessSASkimming\DVRPC_ABM\scenario\Output'
outfile = os.path.join(base_path, 'TripsByTIM2Purpose.csv')

names = ['per', 'trip']
fps = [os.path.join(base_path, '_person_2.dat'), os.path.join(base_path, '_trip_2.dat')]
tables = ReadTables(names, fps, 2*['\t'])
tables['trip']['tim2purp'] = classify_tim2_purposes(tables['per'], tables['trip'])

dvrpc_trips = tables['trip'].query('otaz < 50000 and dtaz < 50000')

trips_by_tim2_purp = dvrpc_trips[['tim2purp', 'trexpfac']].groupby('tim2purp').sum()
trips_by_tim2_purp.to_csv(outfile)
Popen(outfile, shell = True)