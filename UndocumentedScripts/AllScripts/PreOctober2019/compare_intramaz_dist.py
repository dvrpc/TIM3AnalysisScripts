import pandas as pd
import numpy as np
import time
import sys
sys.path.append(r'D:\TIM3')
from daysim_loader import load_daysim_files

before_path = r'T:\TIM_3.1\190712_FullTest\scenario\Output'
before_path = r'Y:\TIM_3.1\DVRPC_ABM_VISUM18patch\scenario\Output'
after_path = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output'

def average_trip_length(trip_data):
    return np.average(trip_data['travdist'], weights = trip_data['trexpfac'])

print('Reading Files')
t0 = time.time()
before = load_daysim_files(before_path)
t1 = time.time()
print('Before files read in ' + str(round(t1-t0,1)) + ' seconds')
after = load_daysim_files(after_path)
t2 = time.time()
print('After files read in ' + str(round(t2-t1,1)) + ' seconds')

print('Calculating intra-parcel distances')
before_ip = before['trip'].query('opcl == dpcl')
after_ip = after['trip'].query('opcl == dpcl')
before_ip_atl = average_trip_length(before_ip)
after_ip_atl = average_trip_length(after_ip)

print('\n')

print('Average Intra-MAZ Trip Length')
print('-----------------------------')
print('Before: ' + str(round(before_ip_atl, 3)))
print('After:  ' + str(round(after_ip_atl, 3)))
print('\n')

print('Number of Linked Transit Trips')
print('------------------------------')
print('Before: ' + str(before['trip'][['mode', 'trexpfac']].query('mode == 6')['trexpfac'].sum()))
print('After:  ' + str(after['trip'][['mode', 'trexpfac']].query('mode == 6')['trexpfac'].sum()))