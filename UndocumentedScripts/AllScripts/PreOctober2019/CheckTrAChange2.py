import pandas as pd
import numpy as np
import time
import sys
from collections import OrderedDict
sys.path.append(r'D:\TIM3')
from daysim_loader import load_daysim_files

before_path = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output'
after_path = r'T:\TIM_3.1\190909_AssignmentConv1e-4\scenario\Output'
taz2county_file = r'D:\TIM3\taz2county.csv'
outfile = r'D:\TIM3\ToPnR_Raw.xlsx'

def get_drive2transit_by_county(files):
    
    hhtour = files['hh'].merge(files['tour'], on = 'hhno')
    drive2transitwork = hhtour[['hhcounty', 'pdpurp', 'tmodetp', 'toexpfac']].query('pdpurp == 1 and tmodetp == 7')
    return drive2transitwork.groupby('hhcounty').sum()['toexpfac']

def get_diff(df, before_col, after_col):
    df['Difference'] = df[after_col] - df[before_col]
    df['% Difference'] = df['Difference'] / df[before_col]

########## MAIN SCRIPT ##########

print('Reading Files')
t0 = time.time()
before = load_daysim_files(before_path)
t1 = time.time()
print('Before files read in ' + str(round(t1-t0,1)) + ' seconds')
after = load_daysim_files(after_path)
t2 = time.time()
print('After files read in ' + str(round(t2-t1,1)) + ' seconds')

print('Reading TAZ to County File')
taz2county = pd.read_csv(taz2county_file, index_col = 0)['County']

print('Getting subset of trips to PnR zones')
toPnR = OrderedDict()
pnr_query = 'dtaz >= 90000 and dtaz <= 92000 and mode in [3, 4, 5]'
toPnR['Before'] = before['trip'].query(pnr_query)
toPnR['After'] = after['trip'].query(pnr_query)

print('Getting Number of Desinations and Average Trip Lengths by PnR Zone')
ntrips = pd.DataFrame()
ntrips['zone'] = range(90001, 90205)
atl = ntrips.copy()
att = ntrips.copy()

for run in ['Before', 'After']:
    toPnR[run]['PMT'] = toPnR[run]['travdist'] * toPnR[run]['trexpfac']
    toPnR[run]['PMinT'] = toPnR[run]['travtime'] * toPnR[run]['trexpfac']
    gbzone = toPnR[run][['dtaz', 'PMT', 'PMinT', 'trexpfac']].groupby('dtaz').sum()
    ntrips[run] = ntrips['zone'].map(gbzone['trexpfac']).fillna(0)
    atl[run] = atl['zone'].map(gbzone['PMT']).fillna(0) / ntrips[run]
    att[run] = att['zone'].map(gbzone['PMinT']).fillna(0) / ntrips[run]

print('Calculating Differences')
get_diff(ntrips, 'Before', 'After')
get_diff(atl, 'Before', 'After')
get_diff(att, 'Before', 'After')

print('Writing Outfile')
outdata = OrderedDict()
outdata['Number of Trips'] = ntrips
outdata['Average Trip Length'] = atl
outdata['Average Travel Time'] = att
pd.Panel(outdata).to_excel(outfile)

print('Done')