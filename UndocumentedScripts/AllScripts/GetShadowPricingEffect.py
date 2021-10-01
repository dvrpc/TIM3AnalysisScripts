from dsa_util import *
from subprocess import Popen

before_path = r'Y:\TIM_3.1\TIM31_HigherTransitCoefficients\scenario\Output'
after_path = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output'

outfile = r'D:\TIM3\BeforeAfterSPEmp.csv'

names = ['before', 'after']
fps = [os.path.join(before_path, '_person_2.dat'), os.path.join(after_path, '_person_2.dat')]

tables = ReadTables(names, fps, 2*['\t'])

output = {}
for table in tables:
    workers = tables[table].query('pwtaz > 0')[['pwtaz', 'psexpfac']]
    output[table] = workers.groupby('pwtaz').sum()['psexpfac']

pd.DataFrame(output).to_csv(outfile)
Popen(outfile, shell = True)