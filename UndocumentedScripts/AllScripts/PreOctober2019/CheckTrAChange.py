import pandas as pd
import numpy as np
import time
import sys
sys.path.append(r'D:\TIM3')
from daysim_loader import load_daysim_files

before_path = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output'
after_path = r'T:\TIM_3.1\190909_AssignmentConv1e-4\scenario\Output'
taz2county_file = r'D:\TIM3\taz2county.csv'

def get_drive2transit_by_county(files):
    
    hhtour = files['hh'].merge(files['tour'], on = 'hhno')
    drive2transitwork = hhtour[['hhcounty', 'pdpurp', 'tmodetp', 'toexpfac']].query('pdpurp == 1 and tmodetp == 7')
    return drive2transitwork.groupby('hhcounty').sum()['toexpfac']

########## MAIN SCRIPT ##########

print('Reading Files')
t0 = time.time()
before = load_daysim_files(before_path)
t1 = time.time()
print('Before files read in ' + str(round(t1-t0,1)) + ' seconds')
after = load_daysim_files(after_path)
t2 = time.time()
print('After files read in ' + str(round(t2-t1,1)) + ' seconds')

hhtour_before = before['hh'].merge(before['tour'], on = 'hhno').query('hhtaz < 50000')
hhtour_after = after['hh'].merge(after['tour'], on = 'hhno').query('hhtaz < 50000')

print(hhtour_before.query('tmodetp == 7')['toexpfac'].sum())
print(hhtour_after.query('tmodetp == 7')['toexpfac'].sum())

#print('Reading TAZ to County File')
#taz2county = pd.read_csv(taz2county_file, index_col = 0)['County']

#print('Adding household counties')
#before['hh']['hhcounty'] = before['hh']['hhtaz'].map(taz2county)
#after['hh']['hhcounty'] = after['hh']['hhtaz'].map(taz2county)

#print('Getting number of drive to transit work tours by county')
#results = pd.DataFrame()
#results['Before'] = get_drive2transit_by_county(before)
#results['After'] = get_drive2transit_by_county(after)

#tf = time.time()
#print(tf - t0)
#print(results)