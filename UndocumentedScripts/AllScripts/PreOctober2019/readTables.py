import pandas as pd
import os
import time

base_path = r'D:\Debugging\Runs'
run = 'survey'
hh_file = os.path.join(base_path, run, '_household_2.dat')
per_file = os.path.join(base_path, run, '_person_2.dat')
tour_file = os.path.join(base_path, run, '_tour_2.dat')
trip_file = os.path.join(base_path, run, '_trip_2.dat')

ts = time.time()
hh = pd.read_table(hh_file)
cp1 = time.time()
print(cp1 - ts)

per = pd.read_table(per_file)
cp2 = time.time()
print(cp2 - cp1)

tour = pd.read_table(tour_file)
cp3 = time.time()
print(cp3 - cp2)

trip = pd.read_table(trip_file)
te = time.time()
print(te - cp3)
print(te - ts)