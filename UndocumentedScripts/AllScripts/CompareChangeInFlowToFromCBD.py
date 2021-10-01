import pandas as pd

parcel_file = r'Y:\TIM_3.1\WorkLocCoreCBD\scenario\inputs\parcels_buffered.dat'
parcel = pd.read_csv(parcel_file, ' ')

parcel['cbd'] = ((parcel['hh_1'] + parcel['emptot_1']) > 20000).astype(int).map({1: 'CBD', 0: 'Not CBD'})
cbd_map = parcel.set_index('parcelid')['cbd']

hh_file_1 = r'Y:\TIM_3.1\Temp\scenario\Output\_household_2.dat'
per_file_1 = r'Y:\TIM_3.1\Temp\scenario\Output\_person_2.dat'

hh_file_2 = r'Y:\TIM_3.1\WorkLocCoreCBD\scenario\Output\0222\_household_2.dat'
per_file_2 = r'Y:\TIM_3.1\WorkLocCoreCBD\scenario\Output\0222\_person_2.dat'

hh_file_3 = r'Y:\TIM_3.1\WorkLocCoreCBD\scenario\Output\_household_2.dat'
per_file_3 = r'Y:\TIM_3.1\WorkLocCoreCBD\scenario\Output\_person_2.dat'

hh_1 = pd.read_csv(hh_file_1, '\t')
per_1 = pd.read_csv(per_file_1, '\t')
hh_2 = pd.read_csv(hh_file_2, '\t')
per_2 = pd.read_csv(per_file_2, '\t')
hh_3 = pd.read_csv(hh_file_3, '\t')
per_3 = pd.read_csv(per_file_3, '\t')

workers_1 = hh_1.merge(per_1, on = 'hhno').query('hhincome >= 100000 and pwpcl > 0')
workers_2 = hh_2.merge(per_2, on = 'hhno').query('hhincome >= 100000 and pwpcl > 0')
workers_3 = hh_3.merge(per_3, on = 'hhno').query('hhincome >= 100000 and pwpcl > 0')

workers_1['hhcbd'] = workers_1['hhparcel'].map(cbd_map)
workers_1['pwcbd'] = workers_1['pwpcl'].map(cbd_map)
workers_2['hhcbd'] = workers_2['hhparcel'].map(cbd_map)
workers_2['pwcbd'] = workers_2['pwpcl'].map(cbd_map)
workers_3['hhcbd'] = workers_3['hhparcel'].map(cbd_map)
workers_3['pwcbd'] = workers_3['pwpcl'].map(cbd_map)

flow_1 = workers_1.groupby(['hhcbd', 'pwcbd']).sum()['psexpfac'].reset_index().pivot('hhcbd', 'pwcbd', 'psexpfac')
flow_2 = workers_2.groupby(['hhcbd', 'pwcbd']).sum()['psexpfac'].reset_index().pivot('hhcbd', 'pwcbd', 'psexpfac')
flow_3 = workers_3.groupby(['hhcbd', 'pwcbd']).sum()['psexpfac'].reset_index().pivot('hhcbd', 'pwcbd', 'psexpfac')

print(flow_1)
print(flow_2)
print(flow_3)