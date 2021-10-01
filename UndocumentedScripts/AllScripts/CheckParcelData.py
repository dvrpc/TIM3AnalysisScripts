import pandas as pd
parcel_file = r'B:\model_development\TIM_3.1_2040\scenario\inputs\parcels_buffered.dat'

parcel = pd.read_csv(parcel_file, ' ')
hhbytaz = parcel.groupby('taz_p').sum()['hh_p']

print('Go')