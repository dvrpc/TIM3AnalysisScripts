import pandas as pd
import numpy as np

def sort_list(lst):
    sorted = lst.copy()
    sorted.sort()
    return sorted

def remove_repeat(lst):
    return list(set(lst))

fp2 = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\microzonetostopareadistance.dat'
fp3 = r'B:\model_development\TIM_3.1\scenario\microzonetostopareadistance.dat'
sa2mode_file = r'D:\TIM3\sa2mode.csv'

exclude_bus = True
exclude_lrt = True
only_bus = True

df2 = pd.read_csv(fp2, ' ')
df3 = pd.read_csv(fp3, ' ')
sa2mode = pd.read_csv(sa2mode_file, index_col = 0)['MODE']

df2['mode'] = df2['stopareaid'].map(sa2mode)
df3['mode'] = df3['stopareaid'].map(sa2mode)

if only_bus:
    exclude_bus = False
    exclude_lrt = False
    df2 = df2[df2['mode'] == 'Bus']
    df3 = df3[df3['mode'] == 'Bus']

if exclude_bus:
    df2 = df2[df2['mode'] != 'Bus']
    df3 = df3[df3['mode'] != 'Bus']

if exclude_lrt:
    df2 = df2[df2['mode'] != 'LRT']
    df3 = df3[df3['mode'] != 'LRT']

df2['sa_list'] = df2['stopareaid'].apply(lambda x: [x])
df3['sa_list'] = df3['stopareaid'].apply(lambda x: [x])

samazs2 = df2.groupby('zoneid')['sa_list'].sum().apply(sort_list)
samazs3 = df3.groupby('zoneid')['sa_list'].sum().apply(sort_list)

outdf = pd.DataFrame({'v2': samazs2, 'v3': samazs3})
outdf['match'] = outdf['v2'] == outdf['v3']
outdf['combined'] = (outdf['v2'] + outdf['v3']).apply(remove_repeat)
outdf['n_mismatch'] = (2*(outdf['combined'].apply(len)) - outdf['v2'].apply(len) - outdf['v3'].apply(len))/2

print(outdf['match'].sum())
print(outdf.shape[0])

print('Go')