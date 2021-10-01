import pandas as pd
import numpy as np
import os
import time
import csv
import threading

daysim_output = {}

class DaySimFileReader(threading.Thread):
    
    def __init__(self, fp, name):
        threading.Thread.__init__(self)
        self.fp = fp
        self.name = name

    def run(self):
        global daysim_output
        print('Reading ' + self.name + ' file\n')
        ts = time.time()
        daysim_output[self.name] = pd.read_csv(self.fp, delimiter = '\t')
        te = time.time()
        print(self.name + ' file read in ' + str(round(te-ts, 1)) + ' seconds')

#base_path = r'D:\TIM3\DaySimOutputs1%'
#base_path = r'T:\TIM_3.1\190802_FullTest\scenario\Output'
#base_path = r'T:\TIM_3.1\190712_FullTest\scenario\Output'
#base_path = r'Y:\TIM_3.1\DVRPC_ABM_022819\scenario\Output'
#base_path = r'T:\TIM_3.1\190806_NewDaySim\scenario\Output'
base_path = r'R:\Model_Development\TIM_3.1\scenario\Output'
hhfile = os.path.join(base_path, '_household_2.dat')
perfile = os.path.join(base_path, '_person_2.dat')
tourfile = os.path.join(base_path, '_tour_2.dat')
tripfile = os.path.join(base_path, '_trip_2.dat')
taz2county_file = os.path.join(r'D:/TIM3/taz2county.csv')
taz2county = pd.read_csv(taz2county_file, index_col = 0)['County']

readers = [DaySimFileReader(hhfile, 'household'),
           DaySimFileReader(perfile, 'person'),
           DaySimFileReader(tourfile, 'tour'),
           DaySimFileReader(tripfile, 'trip')]

#cp0 = time.time()
for reader in readers:
    reader.start()
#cp1 = time.time()
#print('Checkpoint 1: ' + str(cp1-cp0))
for reader in readers:
    reader.join()
#cp2 = time.time()
#print('Checkpoint 2: ' + str(cp2-cp1))



hh = daysim_output['household']
per = daysim_output['person']
tour = daysim_output['tour']
trip = daysim_output['trip']
del daysim_output

hhper = hh[['hhno', 'hhtaz']].merge(per[['hhno', 'pno', 'pwtaz']], on = 'hhno')
pertrip = hhper[['hhno', 'pno', 'hhtaz', 'pwtaz']].merge(trip[['hhno', 'pno', 'dpurp', 'dtaz', 'trexpfac']], on = ['hhno', 'pno'])
not_usual_work = pertrip[['dpurp', 'pwtaz', 'dtaz', 'trexpfac']].query('dpurp == 1 and pwtaz != hhtaz and pwtaz != dtaz')
not_usual_work['dcounty'] = not_usual_work['dtaz'].map(taz2county)

nonusual_work_county_dest = not_usual_work[['dcounty', 'trexpfac']].groupby('dcounty').sum()['trexpfac']
print(nonusual_work_county_dest)
nonusual_work_county_dest.to_csv(r'D:\TIM3\NotUsualWorkCountyDests.csv')

print('Done')