import pandas as pd
import numpy as np
import time
import sys
from collections import OrderedDict
sys.path.append(r'D:\TIM3')
from daysim_loader import load_daysim_files

base_path = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output'

print('Reading Files')
t0 = time.time()
files = load_daysim_files(base_path)
t1 = time.time()
print('Before files read in ' + str(round(t1-t0,1)) + ' seconds')

tourtrip = files['tour'].merge(files['trip'], on = ['hhno', 'pno', 'day', 'tour'])
pnr = tourtrip.query('tmodetp == 7')

print('Go')
