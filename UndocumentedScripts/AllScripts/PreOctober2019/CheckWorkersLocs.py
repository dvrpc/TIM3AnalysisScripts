import pandas as pd
import numpy as np
import os
from subprocess import Popen

wd = os.path.split(__file__)[0]

taz_file = os.path.join(wd, 'taz2county.csv')
taz = pd.read_csv(taz_file, index_col = 0)

runs = ['PopGen', 'Run0', 'Run1a', 'Run2a']

hh = {'PopGen': '_DVRPC_hrec.dat',
      'Run0': r'Runs\run0\_household_2.dat',
      'Run1a': r'Runs\run1a\_household_2.dat',
      'Run2a': r'Runs\run2a\_household_2.dat'}

per = {'PopGen': '_DVRPC_prec.dat',
       'Run0': r'Runs\run0\_person_2.dat',
       'Run1a': r'Runs\run1a\_person_2.dat',
       'Run2a': r'Runs\run2a\_person_2.dat'}

sep = {'PopGen': '\ ',
       'Run0': '\t',
       'Run1a': '\t',
       'Run2a': '\t'}

WorkerLocs = pd.DataFrame(np.zeros((len(taz.index), len(runs))), index = taz.index, columns = runs)

for run in runs:
    hh_file = os.path.join(wd, hh[run])
    per_file = os.path.join(wd, per[run])
    run_hh = pd.read_table(hh_file, sep[run], usecols = ['hhno', 'hhtaz'])
    run_per = pd.read_table(per_file, sep[run], usecols = ['hhno', 'pwtyp', 'psexpfac'])

    run_per['hhtaz'] = run_per['hhno'].map(run_hh.set_index('hhno')['hhtaz'])
    workers = run_per[run_per['pwtyp'] != 0]
    WorkerLocs[run] += workers.groupby('hhtaz').sum()['psexpfac']

outfile = os.path.join(wd, 'WorkerResLocs.csv')
WorkerLocs.fillna(0).to_csv(outfile)
Popen(outfile, shell = True)