import pandas as pd
import os

fps = {}
fps[2015] = r'T:\TIM_3.1\DVRPC_ABM_Github\scenario\inputs\parcels_buffered.dat'
fps[2040] = r'B:\model_development\TIM_3.1_2040\Tools\netbuffer\output\parcels_out.csv'
taz2county_file = r'D:\ref\taz2fips.csv'
taz2county = pd.read_csv(taz2county_file, index_col = 0)['STATE_COUNTY_ID']

counties = taz2county.value_counts().sort_index().index

for year in fps:
    parcel = pd.read_csv(fps[year], ' ')
    parcel['county'] = parcel['taz_p'].map(taz2county)
    outdata = parcel[['county', 'hh_p', 'emptot_p']].groupby('county').sum()
    outdata.to_csv(r'D:\TIM3\HHEmp{}.csv'.format(year))

print('Done')