import pandas as pd
import os

mznode_0 = pd.read_csv(r'Y:\TIM_3.1\PnR_Test\scenario\inputs_dummy\corr_mznode.dat', ' ')
mznode_1 = pd.read_csv(r'Y:\TIM_3.1\PnR_Test\scenario\corr_mznode.dat', ' ')
parcel_0 = pd.read_csv(r'Y:\TIM_3.1\PnR_Test\scenario\inputs_dummy\parcels_buffered.dat', ' ')
parcel_1 = pd.read_csv(r'Y:\TIM_3.1\PnR_Test\scenario\inputs\parcels_buffered.dat', ' ')

print('Min')
print('Parcel: {}'.format((parcel_1 - parcel_0).min().min()))
print('mznode: {}'.format((mznode_1 - mznode_0).min().min()))

print('\n')

print('Max')
print('Parcel: {}'.format((parcel_1 - parcel_0).max().max()))
print('mznode: {}'.format((mznode_1 - mznode_0).max().max()))