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

runs = ['survey', 'run0', 'run1a', 'run2a']

extra_crossings = {}

for run in runs:

    run_path = os.path.join(base_path, 'Runs', run)
    tour_file = os.path.join(run_path, '_tour_2.dat')
    trip_file = os.path.join(run_path, '_trip_2.dat')

    print('Reading tour data from ' + run)
    tour_file = os.path.join(base_path, 'Runs', run, '_tour_2.dat')
    tour = pd.read_table(tour_file, usecols = ['hhno', 'pno', 'day', 'tour', 'pdpurp', 'totaz', 'tdtaz', 'toexpfac'])
    tour['id'] = tour['tour'] + 10*tour['day'] + 100*tour['pno'] + 10000*tour['hhno']
    
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

    print('Reading trip data from ' + run)
    trip = pd.read_table(trip_file, usecols = ['hhno', 'pno', 'day', 'tour', 'otaz', 'dtaz'])
    trip['id'] = trip['tour'] + 10*trip['day'] + 100*trip['pno'] + 10000*trip['hhno']

    print('Identifying counties')
    trip['ocounty'] = trip['otaz'].map(taz2fips).fillna('0').astype(int).astype(str)
    trip['dcounty'] = trip['dtaz'].map(taz2fips).fillna('0').astype(int).astype(str)

    print('Removing null counties')
    trip = trip[trip['ocounty'] != '0']
    trip = trip[trip['dcounty'] != '0']

    print('Identifying origins and destinations in New Jersey')
    trip['onj'] = trip['ocounty'].apply(in_nj)
    trip['dnj'] = trip['dcounty'].apply(in_nj)

    print('Identifying trips crossing the river')
    trip['crossing'] = (trip['onj'] + trip['dnj']) % 2

    print('Grouping trips by tour')
    crossings_by_tour = trip[['id', 'crossing']].groupby('id').sum()['crossing']
    tour['tcrossings'] = tour['crossing']*2 #Theoretical tour crossings
    tour['crossings'] = tour['id'].map(crossings_by_tour)
    tour = tour.dropna()
    tour['extra_crossing'] = tour['crossings'] - tour['tcrossings']

    extra_crossings = tour['extra_crossing'].value_counts()

    print(extra_crossings)
    print('Total Extra Crossings: {}'.format(np.dot(extra_crossings.index, extra_crossings.values)))
    extra_crossings[run] = extra_crossings