import pandas as pd
import numpy as np

def negate(input):
    return not input

infile = r'D:\TIM3.1\TransitSubmodeDiscountTesting\scenario\microzonetostopareadistance.dat'
sa2mode_file = r'D:\TIM3\sa2mode.csv'
outfile = r'D:\TIM3.1\TransitSubmodeDiscountTesting\scenario\maz2sa_top10bus.dat'

sa2mode = pd.read_csv(sa2mode_file, index_col = 0)['MODE']
df = pd.read_csv(infile, ' ')

df['mode'] = df['stopareaid'].map(sa2mode)
df = df.sort_values(['mode', 'zoneid', 'distance'])
df['newzonemode'] = np.concatenate(([1], np.diff(df['zoneid']))).astype(bool)
df['bus'] = df['mode'] == 'Bus'
df['newbus'] = df['newzonemode'] & df['bus']
df['busrank'] = np.zeros_like(df.index)

df = df.reset_index()
del df['index']

newbusix = np.array(df[df['newbus'] == True].index)
for i in range(10, 0, -1):
    df.loc[newbusix + (i-1), 'busrank'] = i

df['ranked'] = df['busrank'] != 0
df['tokeep'] = df['newzonemode'] | df['ranked']

print('Writing output')
df[df['tokeep']][['zoneid', 'stopareaid', 'distance']].to_csv(outfile, ' ', index = False)

print('Go')