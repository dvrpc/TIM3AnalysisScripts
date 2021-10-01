import pandas as pd
import numpy as np
import time
import sys
sys.path.append(r'D:\TIM3')
from daysim_loader import load_daysim_files

#before_path = r'D:\TIM3\DVRPC_Github_Outputs\backup'
#after_path = r'D:\TIM3\DVRPC_Github_Outputs'
before_path = r'B:\model_development\190917_TestDSCorrect\scenario\Output\backup'
after_path = r'B:\model_development\190917_TestDSCorrect\scenario\Output'

print('Reading Files')
t0 = time.time()
before = load_daysim_files(before_path)
t1 = time.time()
print('Before files read in ' + str(round(t1-t0,1)) + ' seconds')
after = load_daysim_files(after_path)
t2 = time.time()
print('After files read in ' + str(round(t2-t1,1)) + ' seconds')

tourtrip = before['tour'][['hhno', 'pno', 'day', 'tour', 'tmodetp', 'totaz', 'tdtaz']].merge(before['trip'][['hhno', 'pno', 'day', 'tour', 'otaz', 'dtaz', 'opurp', 'dpurp', 'mode', 'deptm']], on = ['hhno', 'pno', 'day', 'tour'])
philly2cc = tourtrip.query('tmodetp == 7 and totaz < 2400 and tdtaz < 400')

print('Go')