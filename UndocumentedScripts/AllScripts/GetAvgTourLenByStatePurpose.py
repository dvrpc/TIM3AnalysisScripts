import pandas as pd
import os
import time

base_path = r'Y:\TIM_3.1\DVRPC_ABM_Template\scenario\Output'
hh_file = os.path.join(base_path, '_household_2.dat')
tour_file = os.path.join(base_path, '_tour_2.dat')

t0 = time.time()
hh = pd.read_csv(hh_file, '\t')
tour = pd.read_csv(tour_file, '\t')
t1 = time.time()

order = ['Phila', 'Sub PA', 'Sub NJ', 'Extended']

zone_map = {}
for i in range(4000):
    zone_map[i] = 'Phila'
for i in range(4000, 18000):
    zone_map[i] = 'Sub PA'
for i in range(18000, 30000):
    zone_map[i] = 'Sub NJ'
for i in range(50000, 60000):
    zone_map[i] = 'Extended'

#Filter out non-DVRPC households
tour['hhtaz'] = tour['hhno'].map(hh.set_index('hhno')['hhtaz'])
tour = tour.query('hhtaz < 50000')

tour['district'] = tour['totaz'].map(zone_map)
tour['num'] = tour['tautodist']*tour['toexpfac']
gb_district_purp = tour[['district', 'pdpurp', 'num', 'toexpfac']].groupby(['district', 'pdpurp']).sum()
avg_tour_lengths = (gb_district_purp['num'] / gb_district_purp['toexpfac']).reset_index().pivot('district', 'pdpurp', 0).fillna(0)
n_tours = gb_district_purp['toexpfac'].reset_index().pivot('district', 'pdpurp', 'toexpfac').fillna(0)
for p in range(1, 8):
    avg_tour_lengths['N_%s'%(p)] = n_tours[p]

outfile = r'D:\TIM3\avg_tour_lengths_by_purpose.csv'
avg_tour_lengths.loc[order].to_csv(outfile)

t2 = time.time()

print('Done')
print(t1 - t0)
print(t2 - t1)