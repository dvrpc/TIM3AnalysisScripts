import os
import pandas as pd
import numpy as np
from calibration_util import ReadTables

names = ['tour-base', 'trip-base', 'tour-test', 'trip-test']
fps = [r'D:\TIM3.1\ScriptRename\scenario\Output\_tour_2.dat',
       r'D:\TIM3.1\ScriptRename\scenario\Output\_trip_2.dat',
       r'D:\TIM3.1\RaiseTourRateQuickTest\scenario\Output\_tour_2.dat',
       r'D:\TIM3.1\RaiseTourRateQuickTest\scenario\Output\_trip_2.dat']

tables = ReadTables(names, fps, 4*['\t'])

print('Go')