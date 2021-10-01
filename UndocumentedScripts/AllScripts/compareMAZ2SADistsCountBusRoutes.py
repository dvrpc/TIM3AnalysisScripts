from __future__ import division

import pandas as pd
import numpy as np
from Util import WriteToTrace

def sort_list(lst):
    sorted = lst.copy()
    sorted.sort()
    return sorted

def remove_repeat(lst):
    return list(set(lst))

def add_comma(str):
    return str + ','

fp2 = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\microzonetostopareadistance.dat'
fp3 = r'B:\model_development\TIM_3.1\scenario\microzonetostopareadistance.dat'
sa2mode_file = r'D:\TIM3\sa2mode.csv'
n_mismatch_file = r'D:\TIM3\n_mismatch.csv'

n_mismatch_map = pd.read_csv(n_mismatch_file, index_col = 0, header = None)[1]

exclude_bus = True
exclude_lrt = True
only_bus = True

def split_lines(lines):
    return lines[:-1].split(',')

df2 = pd.read_csv(fp2, ' ')
df3 = pd.read_csv(fp3, ' ')
sa2mode = pd.read_csv(sa2mode_file, index_col = 0)['MODE']

df2['mode'] = df2['stopareaid'].map(sa2mode)
df3['mode'] = df3['stopareaid'].map(sa2mode)

df2 = df2[df2['mode'] == 'Bus']
df3 = df3[df3['mode'] == 'Bus']

sas = np.array(Visum.Net.StopAreas.GetMultiAttValues('No'))[:,1]
sa_lines = np.array(Visum.Net.StopAreas.GetMultiAttValues('Distinct:StopPoints\Distinct:LineRoutes\LineName'))[:, 1]

sa2lines = dict(zip(sas, sa_lines))
df2['lines'] = df2['stopareaid'].map(sa2lines).apply(add_comma)
df3['lines'] = df3['stopareaid'].map(sa2lines).apply(add_comma)

df2['sa_list'] = df2['stopareaid'].apply(lambda x: [x])
df3['sa_list'] = df3['stopareaid'].apply(lambda x: [x])

WriteToTrace(Visum, str(df2.iloc[0]))

samazs2 = df2.groupby('zoneid')[['sa_list', 'lines']].sum()
samazs3 = df3.groupby('zoneid')[['sa_list', 'lines']].sum()

WriteToTrace(Visum, str(samazs2.columns))

WriteToTrace(Visum, str(samazs2['lines'].iloc[0]))

#samazs2['sa_list'] = samazs2['sa_list'].apply(sort_list)
#samazs3['sa_list'] = samazs3['sa_list'].apply(sort_list)

samazs2['lines'] = samazs2['lines'].apply(split_lines).apply(remove_repeat)
samazs3['lines'] = samazs3['lines'].apply(split_lines).apply(remove_repeat)

WriteToTrace(Visum, str(samazs2['lines'].iloc[0]))

samazs2['n_sas'] = samazs2['sa_list'].apply(len)
samazs3['n_sas'] = samazs3['sa_list'].apply(len)
samazs2['n_lines'] = samazs2['lines'].apply(len)
samazs3['n_lines'] = samazs3['lines'].apply(len)

samazs2['n_mismatch'] = samazs2.reset_index()['zoneid'].map(n_mismatch_map)
samazs3['n_mismatch'] = samazs3.reset_index()['zoneid'].map(n_mismatch_map)

WriteToTrace(Visum, str(samazs2['n_lines'].iloc[0]))

outlines = []

for i in range(9):
    outlines.append('')
    outlines.append(str(i))

    query = 'n_mismatch == @i'
    
    try:
        LinesPerMaz2 = samazs2.query(query)['n_lines'].sum() / samazs2.query(query)['n_sas'].sum()
        LinesPerMaz3 = samazs3.query(query)['n_lines'].sum() / samazs3.query(query)['n_sas'].sum()

        outlines.append('v2: ' + str(LinesPerMaz2) + '\nv3: ' + str(LinesPerMaz3))
    except ZeroDivisionError:
        outlines.append('NA\nNA')
outfile = r'D:\TIM3\LinesPerMAZ.txt'
f = open(outfile, 'w')
f.write('\n'.join(outlines))
f.close()