import pandas as pd
import numpy as np
import os

#hh_file = r'R:\Model_Development\TIM_3.1\scenario\Output\_household_2.dat'
#per_file = r'R:\Model_Development\TIM_3.1\scenario\Output\_person_2.dat'
#tour_file = r'R:\Model_Development\TIM_3.1\scenario\Output\_tour_2.dat'

hh_file = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_household_2.dat'
per_file = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_person_2.dat'
tour_file = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_tour_2.dat'

hh = pd.read_csv(hh_file, '\t')
per = pd.read_csv(per_file, '\t')
tour = pd.read_csv(tour_file, '\t')
tour = per.merge(tour, on = ['hhno', 'pno'])

tour['hhtaz'] = tour['hhno'].map(hh.set_index('hhno')['hhtaz'])
#tour = tour.query('totaz != pwtaz')

for p in range(1, 8):
    purp_tour = tour.query('pdpurp == @p')
    print(p, np.average(purp_tour['tautodist'], weights = purp_tour['toexpfac']))

print('Done')