import pandas as pd
import numpy as np
import os

print('Reading 2015')
trip2015 = pd.read_csv(r'D:\TIM3.1\PhoenixvilleSensitivityTest\SP\scenario\Output\_trip_2.dat', '\t').query('mode == 6')
print('Reading 2030')
trip2030 = pd.read_csv(r'D:\TIM3.1\PhoenixvilleSensitivityTest\2030\Base\scenario\Output\_trip_2.dat', '\t').query('mode == 6')

print('Transit Trips')
print('2015: {}'.format(trip2015['trexpfac'].sum()))
print('2030: {}'.format(trip2030['trexpfac'].sum()))
print('\n')

print('Transit Trip Length')
print('2015: {}'.format(np.average(trip2015['travdist'], weights = trip2015['trexpfac'])))
print('2030: {}'.format(np.average(trip2030['travdist'], weights = trip2030['trexpfac'])))