import pandas as pd
import numpy as np

#I copied most of the top from other scripts so there are some fields I create that aren't used
parcel_file = r'D:\TIM3.1\CalibrationApril2021\scenario\inputs\parcels_buffered.dat'
parcel = pd.read_csv(parcel_file, ' ', index_col = 0) #Read in parcel data
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
    parcel['areatype'] = np.where(parcel['areatype{}'.format(i)], i, parcel['areatype']) #Sets the areatype variable to be the area type number

sa2maz_file = r'D:\TIM3.1\CalibrationApril2021\scenario\MAZtoAllStopAreas.csv'
sa2maz = pd.read_csv(sa2maz_file) #Read in MAZ to stop area distance file

#Boolean variables determining if a MAZ is within walking or driving distance from the stop area
sa2maz['walk'] = (sa2maz['dist'] < 0.5*5280)
sa2maz['drive'] = (sa2maz['dist'] < 5*5280)

#Copy MAZ attributes to stop area to MAZ data
sa2maz['hh'] = sa2maz['zoneid'].map(parcel['hh_p'])
sa2maz['emp'] = sa2maz['zoneid'].map(parcel['emptot_p'])
sa2maz['hh+emp'] = sa2maz['hh'] + sa2maz['emp']
sa2maz['areatype'] = sa2maz['zoneid'].map(parcel['areatype'])

sa_areatypes = {}
for access_mode in ['walk', 'drive']:
    data = sa2maz.query(access_mode) #Subset of MAZs accessible to stop areas

    #Create a pivot table with the stop area as the row, the area type as the column, and adding up the number of households
    grouped_data = data.groupby(['stopareaid', 'areatype']).sum()['hh'].reset_index().pivot('stopareaid', 'areatype', 'hh').fillna(0)

    #Identify the area type with the most households for each stop area
    grouped_data['max'] = grouped_data.max(1)
    grouped_data['areatype'] = np.zeros(grouped_data.shape[0], int)
    for i in range(1, 7):
        grouped_data['areatype'] = np.where((grouped_data[i] == grouped_data['max']), i, grouped_data['areatype'])

    sa_areatypes['area_type_' + access_mode] = grouped_data['areatype'].astype(int)

sa_areatypes = pd.DataFrame(sa_areatypes)
sa_areatypes['one'] = np.ones_like(sa_areatypes.index)


sa2at_file = r'D:\ref\sa2area_type.csv'
sa2at = pd.read_csv(sa2at_file, index_col = 0)
sa_areatypes['area_type_taz'] = sa2at['AREATYPE']

gb_sa = sa_areatypes.groupby(['area_type_drive', 'area_type_taz']).sum()['one'].reset_index().pivot('area_type_drive', 'area_type_taz', 'one').fillna(0)
print(gb_sa)
del sa_areatypes['one']
sa_areatypes.to_csv(r'D:\TIM3\StopAreaAreaTypes.csv') #A copy of this table is what is referenced in Summary.xlsx

print('Go')