import os
import pandas as pd
import numpy as np
import time

ts = time.time()

base_path = os.path.split(__file__)[0]
infile = os.path.join(base_path, 'TAZ2SA.xlsx')
taz2sa = pd.read_excel(infile, 'taz2sa')
maz2taz = pd.read_excel(infile, 'maz2taz')

taz2sa['TAZ-SA'] = list(zip(taz2sa['TAZ'], taz2sa['SA']))

zones = np.array(maz2taz['TAZ'].value_counts().sort_index().index)

taz2sa['sa_list'] = taz2sa['SA'].apply(lambda x: [x])
sas_by_taz = taz2sa[['TAZ', 'sa_list']].groupby('TAZ').sum()['sa_list']

for zone in zones:
    if zone not in sas_by_taz.index:
        sas_by_taz.loc[zone] = []

maz2taz['sa_list'] = maz2taz['TAZ'].map(sas_by_taz)
maz2taz['n_sas'] = maz2taz['sa_list'].apply(len)

N = maz2taz['n_sas'].sum()
maz2sa = pd.DataFrame()
maz2sa['zoneid'] = np.repeat(maz2taz['MAZ'], maz2taz['n_sas'])
maz2sa['stopareaid'] = np.hstack(maz2taz['sa_list'].values).astype(int)

maz2sa['TAZ'] = maz2sa['zoneid'].map(maz2taz.set_index('MAZ')['TAZ'])
maz2sa['TAZ-SA'] = list(zip(maz2sa['TAZ'], maz2sa['stopareaid']))
maz2sa['distance'] = maz2sa['TAZ-SA'].map(taz2sa.set_index('TAZ-SA')['LEN_FEET'])

print('Cleaning Up')
del maz2sa['TAZ'], maz2sa['TAZ-SA']

outfile = os.path.join(base_path, 'microzonetostopareadistance.dat')
maz2sa.to_csv(outfile, ' ', index = False)

te = time.time()

print(te - ts)