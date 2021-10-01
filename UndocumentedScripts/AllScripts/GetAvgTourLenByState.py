import pandas as pd

#tour_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\Output\_tour_2.dat'
tour_file = r'D:\TIM3.1\VMTCalibrationJanuary2021\scenario\Output\_tour_2.dat'
tour = pd.read_csv(tour_file, '\t')

zone_map = {}
for i in range(4000):
    zone_map[i] = 'Phila'
for i in range(4000, 18000):
    zone_map[i] = 'Sub PA'
for i in range(18000, 30000):
    zone_map[i] = 'Sub NJ'
for i in range(50000, 60000):
    zone_map[i] = 'Extended'


tour['district'] = tour['totaz'].map(zone_map)
tour['num'] = tour['tautodist']*tour['toexpfac']
gb_district = tour[['district', 'num', 'toexpfac']].groupby('district').sum()
avg_tour_lengths = gb_district['num'] / gb_district['toexpfac']

outfile = r'D:\TIM3\tour_len_new.csv'
avg_tour_lengths.to_csv(outfile)

print('Done')