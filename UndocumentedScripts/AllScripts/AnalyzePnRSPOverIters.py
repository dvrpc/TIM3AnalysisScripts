import pandas as pd
import numpy as np
import os

#base_path = r'D:\TIM3.1\CalibrationApril2021\scenario\Output'
#base_path = r'Y:\TIM_3.1\TestPnRShadowPriceConvergence\scenario\Output'
base_path = r'D:\TIM3.1\TestPnRShadowPriceConvergence\scenario\Output'
outfile = r'D:\TIM3\SPIterProgress0512_TimeSpread60.csv'
outfile_sp = r'D:\TIM3\PricesIter0512_TimeSpread60.csv'

#timestamps = ['2105042055',
#              '2105042237',
#              '2105050020',
#              '2105050203',
#              '2105050345',
#              '2105050528',
#              '2105050712',
#              '2105050855',
#              '2105051042']

#timestamps = ['2105041916',
#              '2105042110',
#              '2105042306',
#              '2105050100',
#              '2105050259',
#              '2105050457',
#              '2105050700',
#              '2105050856',
#              '2105051051',
#              '2105051249']

#timestamps = ['2105051909',
#              '2105052104',
#              '2105052258',
#              '2105060052',
#              '2105060247',
#              '2105060443',
#              '2105060638',
#              '2105060834']

#0507 YOSHI
#timestamps = ['2105071934',
#              '2105072131',
#              '2105072328',
#              '2105080127',
#              '2105080324',
#              '2105080523',
#              '2105080721',
#              '2105080919',
#              '2105081118',
#              '2105081316',
#              '2105081511',
#              '2105081707',
#              '2105081903',
#              '2105082059',
#              '2105082255',
#              '2105090051',
#              '2105090247',
#              '2105090442',
#              '2105090641']

#0505 JFLOOD02 (TimeSpread = 15)
#timestamps = ['2105051906',
#              '2105052050',
#              '2105052232',
#              '2105060015',
#              '2105060159',
#              '2105060342',
#              '2105060525',
#              '2105060712']

#0506 JFLOOD02 (TimeSpread = 30)
#timestamps = ['2105061841',
#              '2105062023',
#              '2105062206',
#              '2105062349',
#              '2105070131',
#              '2105070314',
#              '2105070456',
#              '2105070641']

#0510 JFLOOD02 (Max Penalty = -60, TimeSpread = 5)
#timestamps = ['2105101918',
#              '2105102059',
#              '2105102241',
#              '2105110023',
#              '2105110205',
#              '2105110348',
#              '2105110530',
#              '2105110714']

#0510 YOSHI (Max Penalty = -60, TimeSpread = 30)
#timestamps = ['2105101926',
#              '2105102122',
#              '2105102317',
#              '2105110112',
#              '2105110308',
#              '2105110502',
#              '2105110657',
#              '2105110854',
#              '2105111923',
#              '2105112120',
#              '2105112317',
#              '2105120114',
#              '2105120308',
#              '2105120504',
#              '2105120700',
#              '2105121721',
#              '2105121916',
#              '2105122109',
#              '2105122303',
#              '2105130056',
#              '2105130252',
#              '2105130447',
#              '2105130641',
#              '2105130839',
#              '2105131035']

#0511 JFLOOD (Max Penalty = -60, TimeSpread = 60)
timestamps = ['2105111940',
              '2105112122',
              '2105112304',
              '2105120047',
              '2105120229',
              '2105120411',
              '2105120553',
              '2105120746',
              '2105121734',
              '2105121916',
              '2105122059',
              '2105122243',
              '2105130025',
              '2105130208',
              '2105130350']

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