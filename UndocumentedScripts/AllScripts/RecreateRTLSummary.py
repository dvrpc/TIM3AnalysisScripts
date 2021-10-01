import pandas as pd
import numpy as np
import os

#hh_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\Output\0317\_household_2.dat'
#per_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\Output\0317\_person_2.dat'
#tour_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\Output\0317\_tour_2.dat'
hh_file = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_household_2.dat'
per_file = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_person_2.dat'
tour_file = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_tour_2.dat'

purps = {3: 'Escort',
         4: 'Pers Bus',
         5: 'Shop',
         6: 'Meal',
         7: 'Soc/Rec',
         8: 'Work-Based'}

print('Reading')
hh = pd.read_csv(hh_file, '\t')
per = pd.read_csv(per_file, '\t')
tour = pd.read_csv(tour_file, '\t')

print('Merging')
data = hh.merge(per, on = 'hhno').merge(tour, on = ['hhno', 'pno']).query('hhtaz < 50001')
data['pdpurp2'] = np.where((data['parent'] == 0), data['pdpurp'], 8)

dists = pd.Series()

print('Processing')
for p in purps:
    purp_data = data.query('pdpurp2 == @p')
    dists.loc[purps[p]] = np.average(purp_data['tautodist'], weights = purp_data['toexpfac'])

print(dists)

print('Go')