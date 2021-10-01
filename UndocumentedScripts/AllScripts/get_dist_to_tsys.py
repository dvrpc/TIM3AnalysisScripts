import pandas as pd
import os
import numpy as np

fp = r'B:\model_development\TIM_3.1_Github_0424\scenario\MAZtoAllStopAreas.csv'
df = pd.read_csv(fp)

mode_map = {'BRT': 'ebus',
            'Bus': 'lbus',
            'LRT': 'lrt',
            'Pat': 'crt',
            'Rail': 'crt',
            'Sub': 'fry',
            'Trl': 'lbus'}

df['dsmode'] = df['stopareamode'].map(mode_map).apply(lambda x: 'dist_' + x)

dist = (df.groupby(['zoneid', 'dsmode']).min()['dist']/5280).reset_index().pivot('zoneid', 'dsmode', 'dist').fillna(999)
dist.to_csv(r'D:\TIM3\dist2transit.csv')

print('Done')