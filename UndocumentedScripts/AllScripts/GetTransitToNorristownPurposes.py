import pandas as pd
import numpy as np
import os

zones = list(range(10421, 10434)) + list(range(12401, 12405)) + [12418, 12420]
transit_modes = [6, 7]

base_path = r'Y:\TIM_3.1\PhoenixvilleCalibration\scenario\Output'
tour_file = os.path.join(base_path, '_tour_2.dat')
#trip_file = os.path.join(base_path, '_trip_2.dat')

tour = pd.read_csv(tour_file, '\t')
#trip = pd.read_csv(trip_file, '\t')

transit_to_norristown = tour.query('tmodetp in @transit_modes and tdtaz in @zones and tardest >= 360 and tardest < 600 and tlvdest >= 900 and tlvdest < 1140')
print(transit_to_norristown.groupby('pdpurp').sum()['toexpfac'])