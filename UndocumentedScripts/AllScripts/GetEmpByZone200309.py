from dsa_util import *
from subprocess import Popen

infile = r'B:\model_development\TIM_3.1\scenario\Output\output_0309_SP_6Iter\_person_2.dat'
workers = pd.read_csv(infile, '\t').query('pwtaz > 0')
outdata = workers[['pwtaz', 'psexpfac']].groupby('pwtaz').sum()['psexpfac']

outfile = r'D:\TIM3\WorkLocations200309.csv'
outdata.to_csv(outfile)
Popen(outfile, shell = True)