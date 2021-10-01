import pandas as pd
import numpy as np
import os
import pdb

def add_combined_var(df, var_list):
    to_combine = []
    for var in var_list:
        to_combine.append(df[var].astype(str))
    #pdb.set_trace()
    df['-'.join(var_list)] = list(zip(tuple(to_combine)))
    df['-'.join(var_list)] = df['-'.join(var_list)].apply(lambda x: '-'.join(x))


base_path = r'Y:\TIM_3.1\Temp\scenario\Output'
tour = pd.read_csv(os.path.join(base_path, '_tour_2.dat'), '\t')
trip = pd.read_csv(os.path.join(base_path, '_trip_2.dat'), '\t')

var_list = ['hhno', 'pno', 'day', 'tour', 'half']
#add_combined_var(trip, var_list)
#add_combined_var(tour, var_list[:-1])

trip['halfid'] = list(zip(trip['hhno'], trip['pno'], trip['tour'], trip['half']))
tour['halfid1'] = list(zip(tour['hhno'], tour['pno'], tour['tour'], np.ones_like(tour.index)))
tour['halfid2'] = list(zip(tour['hhno'], tour['pno'], tour['tour'], 2*np.ones_like(tour.index)))


#trips_by_halftour = trip.groupby('halfid').count()['trexpfac']

#tour['half1'] = tour['halfid1'].map(trips_by_halftour)
#tour['half2'] = tour['halfid2'].map(trips_by_halftour)

halftours_by_len = {}
halftours_by_len[1] = tour.groupby('tripsh1').sum()['toexpfac']
halftours_by_len[2] = tour.groupby('tripsh2').sum()['toexpfac']
halftours_by_len = pd.DataFrame(halftours_by_len)
print(halftours_by_len)
print('Go')