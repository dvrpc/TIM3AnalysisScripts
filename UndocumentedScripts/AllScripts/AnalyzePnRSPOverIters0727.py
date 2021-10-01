import pandas as pd
import numpy as np
import os

#base_path = r'D:\TIM3.1\CalibrationApril2021\scenario\Output'
#base_path = r'Y:\TIM_3.1\TestPnRShadowPriceConvergence\scenario\Output'
base_path = r'D:\TIM3.1\CalibrationJuly2021\scenario\Output'
outfile = r'D:\TIM3\SPIterProgress0727.csv'
outfile_sp = r'D:\TIM3\Prices0727.csv'

timestamps = ['2107231830',
              '2107231928',
              '2107232026',
              '2107261655',
              '2107261802',
              '2107261901',
              '2107262000',
              '2107262059',
              '2107262159',
              '2107262259',
              '2107262359',
              '2107270057',
              '2107270352',
              '2107270605',
              '2107270847']

mode_map = {3: 1, 4: 0.5, 5: 0.3}
auto_modes = list(mode_map.keys())

pnr_loads = {}
sp_by_iter = {}
N = len(timestamps)
for i in range(N):
    print('Iter {}'.format(i+1))
    try:
        trip_file = os.path.join(base_path, timestamps[i], '_trip_2.dat')
        trip = pd.read_csv(trip_file, '\t').query('dpurp == 10 and mode in @auto_modes')
        trip['veh_trips'] = trip['mode'].map(mode_map) * trip['trexpfac']
        pnr_loads['Iter {}'.format(i+1)] = trip[['dtaz', 'veh_trips']].groupby('dtaz').sum()['veh_trips']

        sp_file = os.path.join(base_path, timestamps[i], 'park_and_ride_shadow_prices.txt')
        sp = pd.read_csv(sp_file, '\t', index_col = 0)
        prices = pd.DataFrame(np.zeros((180, 1440)), index = range(1, 181))
        for j in range(1440):
            if j < 10:
                prices[j] = sp['PRICE000' + str(j)]
            elif j < 100:
                prices[j] = sp['PRICE00' + str(j)]
            elif j < 1000:
                prices[j] = sp['PRICE0' + str(j)]
            else:
                prices[j] = sp['PRICE' + str(j)]

        sp_by_iter['Iter {}'.format(i+1)] = pd.Series(-prices.min(1), prices.index)

    except IOError:
        continue


print('Writing')
pd.DataFrame(pnr_loads).fillna(0).to_csv(outfile)
pd.DataFrame(sp_by_iter).fillna(0).to_csv(outfile_sp)

print('Done')