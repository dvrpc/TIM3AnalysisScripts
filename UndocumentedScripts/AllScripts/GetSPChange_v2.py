import pandas as pd
import numpy as np
import os
import time
from subprocess import Popen

hh_file = r'T:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\SP\_household_2.dat'
per_file = r'T:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\SP\_person_2.dat'
per_file0 = r'T:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\NoSP\_person_2.dat'
per_file2 = r'T:\TIM_3.1\Sensitivity_Emp\scenario\Output\_person_2.dat'

order = ['Center City', 'Rest of Phila', 'Suburban PA', 'Suburban NJ', 'Extended PA', 'Extended NJ (N)', 'Extended NJ (S)', 'Extended DE/MD']

def pivot_data(data):
    return data.groupby(['wdistrict0', 'wdistrict1']).sum()['psexpfac'].reset_index().pivot('wdistrict0', 'wdistrict1', 'psexpfac').fillna(0).loc[order, order]

def rename_field(df, oldname, newname):
    df[newname] = df[oldname]
    del df[oldname]

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
per2 = pd.read_csv(per_file2, '\t')

hhper = hh.merge(per, on = 'hhno')
hhper0 = hh.merge(per0, on = 'hhno')
hhper2 = hh.merge(per2, on = 'hhno')

hhper0['hhper'] = list(zip(hhper0['hhno'], hhper0['pno']))
pid2oldworkloc = hhper0.set_index('hhper')['pwtaz']

hhper2['hhper'] = list(zip(hhper2['hhno'], hhper2['pno']))
pid2newworkloc = hhper2.set_index('hhper')['pwtaz']

hhper['hhper'] = list(zip(hhper['hhno'], hhper['pno']))
hhper['pwtaz0'] = hhper['pwtaz']
hhper['pwtaz1'] = hhper['hhper'].map(pid2oldworkloc)
hhper['pwtaz2'] = hhper['hhper'].map(pid2newworkloc)

hhper['hdistrict'] = hhper['hhtaz'].map(taz2district)
hhper['wdistrict0'] = hhper['pwtaz0'].map(taz2district)
hhper['wdistrict1'] = hhper['pwtaz1'].map(taz2district)
hhper['wdistrict2'] = hhper['pwtaz2'].map(taz2district)

data = hhper[['hdistrict', 'wdistrict0', 'wdistrict1', 'wdistrict2', 'psexpfac']].dropna()
grouped_data = data.groupby(['hdistrict', 'wdistrict0', 'wdistrict1', 'wdistrict2']).sum()['psexpfac'].reset_index()

#Sort rows to desired order
grouped_data['order_h'] = grouped_data['hdistrict'].apply(lambda x: order.index(x))
grouped_data['order_w0'] = grouped_data['wdistrict0'].apply(lambda x: order.index(x))
grouped_data['order_w1'] = grouped_data['wdistrict1'].apply(lambda x: order.index(x))
grouped_data['order_w2'] = grouped_data['wdistrict2'].apply(lambda x: order.index(x))
grouped_data['order'] = grouped_data[['order_h', 'order_w0', 'order_w1', 'order_w2']].dot([1000, 100, 10, 1])
grouped_data = grouped_data.sort_values('order')
del grouped_data['order_h']
del grouped_data['order_w0']
del grouped_data['order_w1']
del grouped_data['order_w2']
del grouped_data['order']

#Rename columns
rename_field(grouped_data, 'hdistrict', 'Home Location')
rename_field(grouped_data, 'wdistrict0', 'Work Location (No SP)')
rename_field(grouped_data, 'wdistrict1', 'Work Location (SP)')
rename_field(grouped_data, 'wdistrict2', 'Work Location (High CC)')
rename_field(grouped_data, 'psexpfac', 'Number of Workers')

outfile = r'D:\TIM3\ShadowPriceShift2015wCCIncrease.csv'
grouped_data.to_csv(outfile, index = False)
Popen(outfile, shell = True)

#cc = ['Center City']
#phila = cc + ['Rest of Phila']
#dvrpc = phila + ['Suburban PA', 'Suburban NJ']

#out_path = r'D:\TIM3\ShadowPriceCheck2040\ShiftTables'
#pivot_data(data).to_csv(os.path.join(out_path, 'All.csv'))
#pivot_data(data.query('hdistrict in @cc')).to_csv(os.path.join(out_path, 'CenterCity.csv'))
#pivot_data(data.query('hdistrict in @phila')).to_csv(os.path.join(out_path, 'Phila.csv'))
#pivot_data(data.query('hdistrict in @dvrpc')).to_csv(os.path.join(out_path, 'DVRPC.csv'))

print('Done')