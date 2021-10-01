import pandas as pd
import os
from dsa_util import *

base_path = r'T:\TIM_3.1\DVRPC_ABM_Testing\scenario\output'
tables = []
tables.append(DSTable('tour', os.path.join(base_path, '_tour_2.dat'), '\t'))
tables.append(DSTable('trip', os.path.join(base_path, '_trip_2.dat'), '\t'))
tables = ReadTables(table)

