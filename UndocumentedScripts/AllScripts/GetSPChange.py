import pandas as pd
import numpy as np
import os
import time

hh_file = r'B:\model_development\TIM_3.1_2040\scenario\Output\_household_2.dat'
per_file = r'B:\model_development\TIM_3.1_2040\scenario\Output\SP\_person_2.dat'
per_file0 = r'B:\model_development\TIM_3.1_2040\scenario\Output\_person_2.dat'

order = ['Center City', 'Rest of Phila', 'Suburban PA', 'Suburban NJ', 'Extended PA', 'Extended NJ (N)', 'Extended NJ (S)', 'Extended DE/MD']

def pivot_data(data):
    return data.groupby(['wdistrict0', 'wdistrict1']).sum()['psexpfac'].reset_index().pivot('wdistrict0', 'wdistrict1', 'psexpfac').fillna(0).loc[order, order]

ts = time.time()

districts = {'Center City': (1, 200),
             'Rest of Phila': (200, 4000),
             'Suburban PA': (4000, 18000),
             'Suburban NJ': (18000, 50000),
             'Extended PA': (50000, 53000),
             'Extended NJ (N)': (53000, 56000),
             'Extended NJ (S)': (56000, 58000),
             'Extended DE/MD': (58000, 60000)}
taz2district = {}
for i in range(60000):
    for district in districts:
        if i >= districts[district][0] and i < districts[district][1]:
            taz2district[i] = district

te = time.time()
print(te - ts)

hh = pd.read_csv(hh_file, '\t')
per = pd.read_csv(per_file, '\t')
per0 = pd.read_csv(per_file0, '\t')

hhper = hh.merge(per, on = 'hhno')
hhper0 = hh.merge(per0, on = 'hhno')

hhper0['hhper'] = list(zip(hhper0['hhno'], hhper0['pno']))
pid2oldworkloc = hhper0.set_index('hhper')['pwtaz']

hhper['hhper'] = list(zip(hhper['hhno'], hhper['pno']))
hhper['pwtaz0'] = hhper['pwtaz']
hhper['pwtaz1'] = hhper['hhper'].map(pid2oldworkloc)

hhper['hdistrict'] = hhper['hhtaz'].map(taz2district)
hhper['wdistrict0'] = hhper['pwtaz0'].map(taz2district)
hhper['wdistrict1'] = hhper['pwtaz1'].map(taz2district)

data = hhper[['hdistrict', 'wdistrict0', 'wdistrict1', 'psexpfac']].dropna()
cc = ['Center City']
phila = cc + ['Rest of Phila']
dvrpc = phila + ['Suburban PA', 'Suburban NJ']

out_path = r'D:\TIM3\ShadowPriceCheck2040\ShiftTables'
pivot_data(data).to_csv(os.path.join(out_path, 'All.csv'))
pivot_data(data.query('hdistrict in @cc')).to_csv(os.path.join(out_path, 'CenterCity.csv'))
pivot_data(data.query('hdistrict in @phila')).to_csv(os.path.join(out_path, 'Phila.csv'))
pivot_data(data.query('hdistrict in @dvrpc')).to_csv(os.path.join(out_path, 'DVRPC.csv'))

print('Done')