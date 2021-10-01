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
#base_path = r'R:\Model_Development\TIM_3.1\scenario\Output'
base_path = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\0829_SA'
hhfile = os.path.join(base_path, '_household_2.dat')
perfile = os.path.join(base_path, '_person_2.dat')
tourfile = os.path.join(base_path, '_tour_2.dat')
tripfile = os.path.join(base_path, '_trip_2.dat')

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

print('Done')

hh = daysim_output['household']
per = daysim_output['person']
tour = daysim_output['tour']
trip = daysim_output['trip']
del daysim_output

#cp0 = time.time()
#print('Reading Household File')
##hh = dat2df(hhfile)
#hh = pd.read_csv(hhfile, delimiter = '\t')
#cp1 = time.time()
#print('Household File Read in {} seconds'.format(round(cp1-cp0, 1)))

#print('Reading Person File')
##per = dat2df(perfile)
#per = pd.read_csv(perfile, delimiter = '\t')
#cp2 = time.time()
#print('Person File Read in {} seconds'.format(round(cp2-cp1, 1)))

#print('Reading Tour File')
##tour = dat2df(tourfile)
#tour = pd.read_csv(tourfile, delimiter = '\t')
#cp3 = time.time()
#print('Tour File Read in {} seconds'.format(round(cp3-cp2, 1)))

#print('Reading Trip File')
##trip = dat2df(tripfile)
#trip = pd.read_csv(tripfile, delimiter = '\t')
#cp4 = time.time()
#print('Trip File Read in {} seconds'.format(round(cp4-cp3, 1)))

#print('DaySim Files Read in {} seconds'.format(round(cp4-cp0, 1)))

#auto_map = {3: 1,
#            4: 0.5,
#            5: 0.3}

#trip['AutoWeight'] = trip['mode'].map(auto_map)
#print(trip.dropna(subset = ['AutoWeight'])['trexpfac'].sum())
#print(trip[['mode', 'otaz', 'dtaz', 'travdist', 'travtime']].query('mode in [3, 4, 5] and otaz == 55506 and dtaz == 52001')[['travdist', 'travtime']])

#intra_dvrpc = trip[['mode', 'otaz', 'dtaz', 'travdist', 'travtime']].query('mode in [3, 4, 5] and otaz < 50000 and dtaz < 50000')
#extended_dvrpc = trip[['mode', 'otaz', 'dtaz', 'travdist', 'travtime']].query('mode in [3, 4, 5] and ((otaz >= 50000 and dtaz < 50000) or (otaz < 50000 and dtaz >= 50000))')
#extended_extended = trip[['mode', 'otaz', 'dtaz', 'travdist', 'travtime']].query('mode in [3, 4, 5] and otaz >= 50000 and dtaz >= 50000')

#print(intra_dvrpc[['travdist', 'travtime']].describe())
#print(extended_dvrpc[['travdist', 'travtime']].describe())
#print(extended_extended[['travdist', 'travtime']].describe())