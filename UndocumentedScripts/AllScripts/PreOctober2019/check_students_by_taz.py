import pandas as pd
import os
from subprocess import Popen

runs = ['run0', 'run1a', 'run2a']

students_by_taz = pd.DataFrame()
BASE_PATH = r'D:\Debugging\Runs'
for run in runs:
    per = pd.read_table(os.path.join(BASE_PATH, run, '_person_2.dat'), usecols = ['pstaz', 'psexpfac'])
    students_by_taz[run] = per.groupby('pstaz').sum()['psexpfac']

outfile = os.path.join(BASE_PATH, 'studentsByTAZ.csv')
students_by_taz.fillna(0).to_csv(outfile)
Popen(outfile, shell = True)