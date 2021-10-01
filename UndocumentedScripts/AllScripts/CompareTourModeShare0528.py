import pandas as pd
import numpy as np
import os

paths = {'survey': r'D:\TIM3.1\VersionWithSurveyData\scenario\Output',
         'daysim': r'D:\TIM3.1\CalibrationJune2021\scenario\Output'}

mode_trips = {}
for set in paths:
    print(set)
    hh = pd.read_csv(os.path.join(paths[set], '_household_2.dat'), '\t')
    tour = hh[['hhno', 'hhtaz']].merge(pd.read_csv(os.path.join(paths[set], '_tour_2.dat'), '\t'),
                                              on = 'hhno').query('hhtaz < 50000')
    mode_trips[set] = tour[['tmodetp', 'toexpfac']].groupby('tmodetp').sum()['toexpfac']

pd.DataFrame(mode_trips).to_csv(r'D:\TIM3\TourShare0528.csv')

print('Done')