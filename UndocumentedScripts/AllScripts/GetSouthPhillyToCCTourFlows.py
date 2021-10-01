import pandas as pd
import numpy as np
import os
from collections import OrderedDict as od

survey_path = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output'
daysim_path = r'R:\Model_Development\TIM_3.1\scenario\Output'

def ReadTour(base_path):
    hh = pd.read_csv(os.path.join(base_path, '_household_2.dat'), '\t')
    tour = pd.read_csv(os.path.join(base_path, '_tour_2.dat'), '\t')
    tour['hhtaz'] = tour['hhno'].map(hh.set_index('hhno')['hhtaz'])
    return tour.query('hhtaz < 50000')

tables = od()
tables['Survey'] = ReadTour(survey_path)
tables['DaySim'] = ReadTour(daysim_path)

sp2cc = pd.DataFrame(index = range(1, 8))
for table in tables:
    sp2cc[table] = tables[table].query('(totaz >= 1800 and totaz < 2000 and tdtaz < 200)').groupby('pdpurp').sum()['toexpfac']

print(sp2cc.fillna(0))