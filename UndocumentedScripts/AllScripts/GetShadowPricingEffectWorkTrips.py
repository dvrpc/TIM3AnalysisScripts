from dsa_util import *
from subprocess import Popen

before_path = r'Y:\TIM_3.1\TIM31_HigherTransitCoefficients\scenario\Output'
after_path = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output'

outfile = r'D:\TIM3\BeforeAfterSPWTEnds.csv'

names = ['before', 'after']
fps = [os.path.join(before_path, '_trip_2.dat'), os.path.join(after_path, '_trip_2.dat')]

tables = ReadTables(names, fps, 2*['\t'])

output = {}
for table in tables:
    workers = tables[table].query('dpurp == 1')[['dtaz', 'trexpfac']]
    output[table] = workers.groupby('dtaz').sum()['trexpfac']

pd.DataFrame(output).to_csv(outfile)
Popen(outfile, shell = True)