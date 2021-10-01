import pandas as pd
import numpy as np
import time
import sys
sys.path.append(r'D:\TIM3')
from daysim_loader import load_daysim_files

#before_path = r'D:\TIM3\DVRPC_Github_Outputs\backup'
#after_path = r'D:\TIM3\DVRPC_Github_Outputs'
before_path = r'Y:\TIM_3.1\DVRPC_ABM_190910\scenario\Output'
after_path = r'B:\model_development\TIM_3.1\scenario\Output'

print('Reading Files')
t0 = time.time()
before = load_daysim_files(before_path)
t1 = time.time()
print('Before files read in ' + str(round(t1-t0,1)) + ' seconds')
after = load_daysim_files(after_path)
t2 = time.time()
print('After files read in ' + str(round(t2-t1,1)) + ' seconds')

n_before = before['trip']['trexpfac'].sum()
n_after = after['trip']['trexpfac'].sum()

print(before['trip'][['mode', 'trexpfac']].groupby('mode').sum()['trexpfac'] / n_before)
print(after['trip'][['mode', 'trexpfac']].groupby('mode').sum()['trexpfac'] / n_after)

print(n_before)
print(n_after)

print('Go')