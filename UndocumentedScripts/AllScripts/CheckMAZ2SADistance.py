import pandas as pd

fp1 = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\MAZtoAllStopAreas.csv'
fp2 = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\microzonetostopareadistance_1milecutoff.dat'

df1 = pd.read_csv(fp1)
df2 = pd.read_csv(fp2, ' ')

df1['maz-sa'] = list(zip(df1['zoneid'], df1['stopareaid']))
df2['maz-sa'] = list(zip(df2['zoneid'], df2['stopareaid']))

df2 = df2.sort_values('distance', ascending = True).drop_duplicates(subset = ['maz-sa'])
df1['old_dist'] = df1['maz-sa'].map(df2.set_index('maz-sa')['distance'])
df1 = df1.dropna(subset = ['old_dist'])

df1['change'] = df1['dist'] - df1['old_dist']
df1['% change'] = df1['change'] / df1['old_dist']

print('Go')