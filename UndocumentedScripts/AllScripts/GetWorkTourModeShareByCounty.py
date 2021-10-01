import pandas as pd
import numpy as np
import os

base_path = r'B:\model_development\TIM_3.1_Github_Copy\scenario\output'
hh_file = os.path.join(base_path, '_household_2.dat')
per_file = os.path.join(base_path, '_person_2.dat')
tour_file = os.path.join(base_path, '_tour_2.dat')

def pivot(df, rows, columns, values):
    return df[[rows, columns, values]].groupby([rows, columns]).sum()[values].reset_index().pivot(rows, columns, values).fillna(0)

def combine_transit(df):
    df[6] = df[6] + df[7]
    del df[7]
    return df

county_map = {}
for i in range(4000):
    county_map[i] = 'Philadelphia'
for i in range(4000, 6000):
    county_map[i] = 'Delaware'
for i in range(6000, 10000):
    county_map[i] = 'Chester'
for i in range(10000, 14000):
    county_map[i] = 'Montgomery'
for i in range(14000, 18000):
    county_map[i] = 'Bucks'
for i in range(18000, 20000):
    county_map[i] = 'Mercer'
for i in range(20000, 22000):
    county_map[i] = 'Burlington'
for i in range(22000, 24000):
    county_map[i] = 'Camden'
for i in range(24000, 28000):
    county_map[i] = 'Gloucester'

hh = pd.read_csv(hh_file, '\t')
#per = pd.read_csv(per_file, '\t')
tour = pd.read_csv(tour_file, '\t')

tour['hhtaz'] = tour['hhno'].map(hh.set_index('hhno')['hhtaz'])
tour['hhcounty'] = tour['hhtaz'].map(county_map)

work_tours = tour.query('pdpurp == 1')
work_tours_to_phila = work_tours.query('tdtaz < 4000')

all_mode_tours = combine_transit(pivot(work_tours, 'hhcounty', 'tmodetp', 'toexpfac'))
phila_mode_tours = combine_transit(pivot(work_tours_to_phila, 'hhcounty', 'tmodetp', 'toexpfac'))

order = ['Philadelphia', 'Delaware', 'Chester', 'Montgomery', 'Bucks', 'Mercer', 'Burlington', 'Camden', 'Gloucester']

outfile = r'D:\TIM3\WorkTourModeTrips0416_Raw.xlsx'
writer = pd.ExcelWriter(outfile)
all_mode_tours.loc[order].to_excel(writer, 'All')
phila_mode_tours.loc[order].to_excel(writer, 'Phila')
writer.close()

print('Go')