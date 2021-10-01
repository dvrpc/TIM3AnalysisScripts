import pandas as pd
import numpy as np
import os

fp0 = r'D:\TIM3.1\191217_DistToTransit0\scenario\Output\_trip_2.dat'
fp1 = r'D:\TIM3.1\200121_RemoveAlogitJunk\scenario\Output\_trip_2.dat'

trip0 = pd.read_csv(fp0, '\t')
trip1 = pd.read_csv(fp1, '\t')

#Trips by mode
tbm0 = trip0[['mode', 'trexpfac']].groupby('mode').sum()['trexpfac']
tbm1 = trip1[['mode', 'trexpfac']].groupby('mode').sum()['trexpfac']
trips_by_mode = pd.DataFrame({'Base': tbm0, 'Test': tbm1})
print(trips_by_mode)

#Trips by destination purpose
tbp0 = trip0[['dpurp', 'trexpfac']].groupby('dpurp').sum()['trexpfac']
tbp1 = trip1[['dpurp', 'trexpfac']].groupby('dpurp').sum()['trexpfac']
trips_by_purpose = pd.DataFrame({'Base': tbp0, 'Test': tbp1})
print(trips_by_purpose)