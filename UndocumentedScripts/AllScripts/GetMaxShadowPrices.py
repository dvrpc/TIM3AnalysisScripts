import pandas as pd
import numpy as np

sp_file = r'D:\TIM3.1\CalibrationApril2021\scenario\working\park_and_ride_shadow_prices.txt'
pnr_file = r'D:\TIM3.1\CalibrationApril2021\scenario\inputs\DVRPC_p_rNodes.dat'

sp = pd.read_csv(sp_file, '\t', index_col = 0)
pnr = pd.read_csv(pnr_file, '\t', index_col = 1)
#pnr['PriceAtMaxTime'] = pnr['NodeID'].map(sp['PRICE0617'])
#pnr['LoadAtMaxTime'] = pnr['NodeID'].map(sp['PRLOAD0617'])
#pnr['Load/Cap'] = pnr['LoadAtMaxTime'] / pnr['Capacity']

#pnr.to_csv(r'D:\TIM3\PnRSPResults.csv')

cols = list(sp.columns)
first_price = cols.index('PRICE0000')
first_load = cols.index('PRLOAD0000')

prices = sp.iloc[:, first_price:first_price+1440]
loads = sp.iloc[:, first_load:first_load+1440]

entries = pd.DataFrame(np.zeros_like(loads), loads.index, loads.columns)
for i in entries.index:
    entries.loc[i] = np.hstack((loads.loc[i, 'PRLOAD0000'], np.diff(loads.loc[i])))

entries = np.where(entries < 0, 0, entries)

print(np.average(prices, weights = entries))

print('Go')