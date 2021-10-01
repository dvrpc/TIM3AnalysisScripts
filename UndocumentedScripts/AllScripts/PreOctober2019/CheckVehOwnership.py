import pandas as pd
import numpy as np

hh_file = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\_household_2.dat'
taz2cpa_file = r'D:\TIM3\taz2cpa.csv'
ctpp_file = r'D:\TIM3\CTPP_PhilaVehOwnership.csv'

hh = pd.read_csv(hh_file, '\t').query('hhtaz < 4000')
taz2cpa = pd.read_csv(taz2cpa_file, index_col = 0)['CPA']
ctpp_data = pd.read_csv(ctpp_file, index_col = 0)
ctpp_data.columns = ctpp_data.columns.astype(int)

hh['CPA'] = hh['hhtaz'].map(taz2cpa)

table = hh[['CPA', 'hhvehs', 'hhexpfac']].groupby(['CPA', 'hhvehs']).sum()['hhexpfac'].reset_index().pivot('CPA', 'hhvehs', 'hhexpfac')

table.loc[102] += table.loc[105]
table = table.drop(105)

results = {'CTPP': ctpp_data, 'DaySim': table}
results = pd.Panel(results)
results['Difference'] = results['DaySim'] - results['CTPP']
results['% Diff'] = results['Difference'] / results['CTPP']

results.to_excel(r'D:\TIM3\PhilaVehOwnership_Raw.xlsx')

print('Go')