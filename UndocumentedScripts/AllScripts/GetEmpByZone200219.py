from dsa_util import *
from subprocess import Popen

names = ['0', '20', '3']
fps = [r'Y:\TIM_3.1\TIM31_HigherTransitCoefficients\scenario\Output\_person_2.dat',
       r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\20Iters\_person_2.dat',
       r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\_person_2.dat']

tables = ReadTables(names, fps, 3*['\t'])

outfile = r'D:\TIM3\ShadowPriceEffect200219.csv'

output = {}
for table in tables:
    workers = tables[table].query('pwtaz > 0')
    output[table] = workers[['pwtaz', 'psexpfac']].groupby('pwtaz').sum()['psexpfac']

pd.DataFrame(output).to_csv(outfile)
Popen(outfile, shell = True)