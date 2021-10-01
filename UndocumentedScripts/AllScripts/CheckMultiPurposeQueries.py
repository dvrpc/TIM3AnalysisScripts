import pandas as pd
import numpy as np
import os

queries = {'dt-work': 'tmodetp == 7',
           'wt-work': 'pdpurp == 1 and tmodetp == 6 and parent == 0',
           'wt-otherHB': 'pdpurp >= 4 and tmodetp == 6 and parent == 0',
           'wt-escort-workbased': 'tmodetp == 6 and (pdpurp == 2 or pdpurp == 3 or parent > 0)'}

tour_file = r'R:\Model_Development\TIM31_PurposeMultiClassAssignment\_tour_2.dat'
trip_file = r'R:\Model_Development\TIM31_PurposeMultiClassAssignment\_trip_2.dat'

print('Reading')
tour = pd.read_csv(tour_file, '\t')
trip = pd.read_csv(trip_file, '\t')

tourtrip = tour.merge(trip, on = ['hhno', 'pno', 'day', 'tour']).query('mode == 6')

#tourtrip['dt-work'] = (tourtrip['tmodetp'] == 7)
#tourtrip['wt-work'] = ((tourtrip['pdpurp'] == 1) & (tourtrip['tmodetp'] == 6) & (tourtrip['parent'] == 0))
#tourtrip['wt-otherHB'] = ((tourtrip['pdpurp'] >= 4) & (tourtrip['tmodetp'] == 6) & (tourtrip['parent'] == 0))
#tourtrip['wt-escort-workbased'] = ((tourtrip['tmodetp'] == 6) & ((tourtrip['pdpurp'] == 2) | (tourtrip['pdpurp'] == 3) | (tourtrip['parent'] > 0)))

print('Processing')

results = pd.DataFrame(np.zeros((4, 4)), queries.keys(), queries.keys())

for qry1 in queries:
    for qry2 in queries:
        results.loc[qry1, qry2] = tourtrip.query('({0}) and ({1})'.format(queries[qry1], queries[qry2]))['trexpfac'].sum()

print(results)