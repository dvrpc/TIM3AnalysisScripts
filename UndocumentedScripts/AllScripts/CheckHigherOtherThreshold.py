import pandas as pd

parcel_file = r'R:\Model_Development\TIM_3.1\scenario\inputs\parcels_buffered.dat'
parcel = pd.read_csv(parcel_file, ' ', index_col = 0)
parcel['OldCoreCBD'] = ((parcel['hh_1'] + parcel['emptot_1']) > 20000).astype(int)
parcel['NewCoreCBD'] = ((parcel['hh_1'] + parcel['emptot_1']) > 31000).astype(int)
parcel['CoreCBDCat'] = (parcel['OldCoreCBD'] + parcel['NewCoreCBD']).map({0: 'NotCoreCBD', 1: 'OldCoreCBD', 2: 'NewCoreCBD'})

base_file = r'R:\Model_Development\TIM_3.1\scenario\Output\Output_Base_0303\_tour_2.dat'
test_file = r'R:\Model_Development\TIM_3.1\scenario\Output\_tour_2.dat'

base = pd.read_csv(base_file, '\t').query('pdpurp >= 4')
test = pd.read_csv(test_file, '\t').query('pdpurp >= 4')

base['dCoreCBDCat'] = base['tdpcl'].map(parcel['CoreCBDCat'])
test['dCoreCBDCat'] = test['tdpcl'].map(parcel['CoreCBDCat'])

gb_cat = {}
gb_cat['Base'] = base.groupby('dCoreCBDCat').sum()['toexpfac']
gb_cat['Test'] = test.groupby('dCoreCBDCat').sum()['toexpfac']
gb_cat = pd.DataFrame(gb_cat)
print(gb_cat)