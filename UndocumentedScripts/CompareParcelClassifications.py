import pandas as pd
import numpy as np
import os

parcel_file = r'D:\TIM3.1\CalibrationJune2021\scenario\inputs\parcels_buffered.dat'
parcel = pd.read_csv(parcel_file, ' ')

taz_file = r'D:\ref\taz_data.csv'
taz = pd.read_csv(taz_file)
taz['district'] = taz.shape[0]*['']
taz['district'] = np.where(taz['STATE_COUNTY_ID'] // 1000 == 34, 'Suburban NJ', taz['district'])
taz['district'] = np.where(taz['STATE_COUNTY_ID'] // 1000 == 42, 'Suburban PA', taz['district'])
taz['district'] = np.where(taz['STATE_COUNTY_ID'] == 42101, 'Rest of Phila', taz['district'])
taz['district'] = np.where((taz['CPA'] == 103) & (taz['AREA_TYPE'] == 1), 'Center City', taz['district'])
taz['district'] = np.where(taz['NO'] > 50000, 'Extended', taz['district'])
taz = taz.set_index('NO')

parcel['subway'] = ((parcel['dist_fry'] > 0) & (parcel['dist_fry'] <= 0.5))
parcel['hh+emp'] = parcel['hh_1'] + parcel['emptot_1']
parcel['areatype1'] = (parcel['hh+emp'] >= 9000)
parcel['areatype2'] = ((parcel['hh+emp'] < 9000) & (parcel['hh+emp'] >= 7800))
parcel['areatype3'] = ((parcel['hh+emp'] < 7800) & (parcel['hh+emp'] >= 2750))
parcel['areatype4'] = ((parcel['hh+emp'] < 2750) & (parcel['hh+emp'] >= 450))
parcel['areatype5'] = ((parcel['hh+emp'] < 450) & (parcel['hh+emp'] >= 40))
parcel['areatype6'] = (parcel['hh+emp'] < 40)
parcel['corecbd'] = (parcel['hh+emp'] >= 31000)
parcel['cbd'] = (parcel['areatype1'] | parcel['areatype2'])
parcel['urban'] = parcel['areatype3']
parcel['suburb'] = parcel['areatype4']
parcel['rural'] = parcel['areatype5'] + parcel['areatype6']
parcel['fringecbd'] = (parcel['cbd']) & (~parcel['corecbd'])
parcel['innj'] = (((parcel['taz_p'] >= 18000) & (parcel['taz_p'] < 50000)) | ((parcel['taz_p'] >= 53000) & (parcel['taz_p'] < 58000)))

parcel['district'] = parcel['taz_p'].map(taz['district'])

districts = ['Center City', 'Rest of Phila', 'Suburban NJ', 'Suburban PA', 'Extended']
vars = ['cbd', 'urban', 'suburb', 'rural', 'subway', 'innj', 'corecbd', 'fringecbd']
M = len(districts)
N = len(vars)

outdata = pd.DataFrame(np.zeros((M, N)), index = districts, columns = vars)
for var in vars:
    outdata[var] += parcel.query(var).groupby('district').sum()['emptot_p']

outdata.fillna(0).T.to_csv(r'D:\TIM3\ParcelDistrictsByAreaTypeEMP.csv')

print('Go')