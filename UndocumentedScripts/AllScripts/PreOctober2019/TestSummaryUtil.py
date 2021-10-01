import os
os.chdir(os.path.dirname(__file__))
from SummaryUtil import *
import time
import re

hh_file = r'D:/TIM3/DaySimOutputs1%/_household_2.dat'
#hh_file = r'Y:\TIM_3.1\DVRPC_ABM_VISUM18patch\scenario\Output\_household_2.dat'
per_file = hh_file.replace('household', 'person')
tour_file = hh_file.replace('household', 'tour')
trip_file = hh_file.replace('household', 'trip')

cp0 = time.time()

hh = df.from_file(hh_file)
cp1 = time.time()
print(100*(cp1-cp0))

per = df.from_file(per_file)
cp2 = time.time()
print(100*(cp2-cp1))

tour = df.from_file(tour_file)
cp3 = time.time()
print(100*(cp3-cp2))

trip = df.from_file(trip_file)
cp4 = time.time()
print(100*(cp4-cp3))
print(100*(cp4-cp0))

print('Go')