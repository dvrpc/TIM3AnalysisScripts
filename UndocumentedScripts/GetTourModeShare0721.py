import pandas as pd
import numpy as np
import os
from collections import OrderedDict

base_path =r'D:\TIM3.1\CalibrationJuly2021\scenario\Output'
runs = ['0719', '0720Test', '0720', '0721Test']
outfile = r'D:\TIM3\TourModeShares0721.csv'

tours_by_mode = OrderedDict()
for run in runs:
    print(run)
    tour = pd.read_csv(os.path.join(base_path, run, '_tour_2.dat'), '\t')
    tours_by_mode[run] = tour.groupby('tmodetp').sum()['toexpfac']

print('Writing')
pd.DataFrame(tours_by_mode).to_csv(outfile)

print('Go')