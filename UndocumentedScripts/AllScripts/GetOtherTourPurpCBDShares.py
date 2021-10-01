import pandas as pd
import os

parcel_file = r'Y:\TIM_3.1\Temp\scenario\inputs\parcels_buffered.dat'
parcel = pd.read_csv(parcel_file, ' ', index_col = 0)
parcel['cbd'] = ((parcel['hh_1'] + parcel['emptot_1']) > 20000).astype(int).map({1: 'CBD', 0: 'NotCBD'})

#base_path = r'Y:\TIM_3.1\Temp\scenario\Output'
base_path = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\Output'
hh_file = os.path.join(base_path, '_household_2.dat')
tour_file = os.path.join(base_path, '_tour_2.dat')
hh = pd.read_csv(hh_file, '\t')
tour = pd.read_csv(tour_file, '\t')

tour['hhtaz'] = tour['hhno'].map(hh.set_index('hhno')['hhtaz'])
tour = tour.query('hhtaz < 50000')
tour['dcbd'] = tour['tdpcl'].map(parcel['cbd'])

for p in range(4, 8):
    print(p)
    grouped = tour.query('pdpurp == @p').groupby('dcbd').sum()['toexpfac']
    print(grouped)
    print('\n')