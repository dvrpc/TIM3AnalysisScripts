import pandas as pd
import numpy as np
import os
from subprocess import Popen

def in_nj(fips):
    '''
    Identifies if a FIPS code is in New Jersey
    '''
    return int(fips[:2] == '34')

base_path = os.path.split(__file__)[0]
taz2fips_file = os.path.join(base_path, 'taz2fips.csv')
taz2fips = pd.read_csv(taz2fips_file, index_col = 0)['STATE_COUNTY_ID']

runs = ['NoRXP', 'WithRXP']
crossings_by_purp = pd.DataFrame(np.zeros((11, len(runs))), index = range(11), columns = runs)
crossings_by_purp.loc['Total'] = np.nan

for run in runs:
    print('Reading data from ' + run)
    tour_file = os.path.join(base_path, 'RunsTIM31', run, '_tour_2.dat')
    tour = pd.read_table(tour_file, usecols = ['pdpurp', 'totaz', 'tdtaz', 'toexpfac'])
    
    print('Identifying counties')
    tour['tocounty'] = tour['totaz'].map(taz2fips).fillna('0').astype(int).astype(str)
    tour['tdcounty'] = tour['tdtaz'].map(taz2fips).fillna('0').astype(int).astype(str)

    print('Removing null counties')
    tour = tour[tour['tocounty'] != '0']
    tour = tour[tour['tdcounty'] != '0']

    print('Identifying origins and destinations in New Jersey')
    tour['tonj'] = tour['tocounty'].apply(in_nj)
    tour['tdnj'] = tour['tdcounty'].apply(in_nj)

    print('Identifying tours crossing the river')
    tour['crossing'] = (tour['tonj'] + tour['tdnj']) % 2
    tour['n_crossing'] = tour['crossing']*tour['toexpfac']

    print('Adding grouped results to summary file')
    result = tour[['pdpurp', 'n_crossing']].groupby('pdpurp').sum()['n_crossing'].sort_index()
    result.loc['Total'] = tour['toexpfac'].sum()
    crossings_by_purp[run] = result

    print('======================================')

outfile = os.path.join(base_path, 'Runs', 'crossings_by_purp.csv')
crossings_by_purp.fillna(0).to_csv(outfile)
Popen(outfile, shell = True)