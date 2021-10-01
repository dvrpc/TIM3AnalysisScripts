import pandas as pd
import numpy as np

#trip_file = r'D:\TIM3\output0411\_trip_2.dat'
trip_file = r'D:\TIM3.1\CalibrationApril2021\scenario\Output\0414Test\_trip_2.dat'
parcel_file = r'D:\TIM3.1\CalibrationApril2021\scenario\inputs\parcels_buffered.dat'

parcel = pd.read_csv(parcel_file, ' ', index_col = 0)
parcel['subway_corr'] = ((parcel['dist_fry'] > 0) & (parcel['dist_fry'] <= 0.5))
parcel['hh+emp'] = parcel['hh_1'] + parcel['emptot_1']
parcel['areatype1'] = (parcel['hh+emp'] >= 31000)
parcel['areatype2'] = ((parcel['hh+emp'] < 31000) & (parcel['hh+emp'] >= 7800))
parcel['areatype3'] = ((parcel['hh+emp'] < 7800) & (parcel['hh+emp'] >= 2750))
parcel['areatype4'] = ((parcel['hh+emp'] < 2750) & (parcel['hh+emp'] >= 450))
parcel['areatype5'] = ((parcel['hh+emp'] < 450) & (parcel['hh+emp'] >= 40))
parcel['areatype6'] = (parcel['hh+emp'] < 40)
parcel['corecbd'] = (parcel['hh+emp'] >= 31000)
parcel['cbd'] = parcel['areatype1'] + parcel['areatype2']
parcel['urban'] = parcel['areatype3']
parcel['suburb'] = parcel['areatype4']
parcel['rural'] = parcel['areatype5'] + parcel['areatype6']
parcel['areatype'] = np.zeros_like(parcel.index)

for i in range(1, 7):
    parcel['areatype'] = np.where(parcel['areatype{}'.format(i)], i, parcel['areatype'])

trip = pd.read_csv(trip_file, '\t')
trip['oareatype'] = trip['opcl'].map(parcel['areatype'])

pnr_zones = [90045, 90088, 90101, 90095, 90165, 90163, 90148, 90109, 90029, 90009, 90155, 90151, 90020, 90077, 90167, 90156, 90170, 90136, 90002, 90001, 90132, 90048]
auto_modes = [3, 4, 5]
pnr_trips = trip.query('dtaz in @pnr_zones and mode in @auto_modes')
#pnr_trips = trip.query('otaz == @pnr_zone and mode == 6')
print(pnr_trips.groupby('oareatype').sum()['trexpfac'])

print('Go')