import pandas as pd
import numpy as np
import os

#base_path = r'D:\TIM3.1\CalibrationApril2021\scenario\Output'
#base_path = r'Y:\TIM_3.1\TestPnRShadowPriceConvergence\scenario\Output'
#base_path = r'D:\TIM3.1\CalibrationAugust2021\scenario\Output'
#base_path = r'Y:\TIM_3.1\DVRPC_ABM_Template\scenario\Output'
base_path = r'D:\TIM3.1\PhoenixvilleSensitivityTest\SP\scenario\Output'
outfile = r'D:\TIM3\SPIterProgress_JFLOOD0817_b.csv'
outfile_sp = r'D:\TIM3\Prices_JFLOOD0817_b.csv'

timestamps = ['2108171342',
              '2108171439',
              '2108171534',
              '2108171631',
              '2108171729',
              '2108171827',
              '2108171925',
              '2108172021',
              '2108172118',
              '2108172215',
              '2108172313',
              '2108180014',
              '2108180112',
              '2108180341',
              '2108180550']

timestamps = ['2108181345']

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