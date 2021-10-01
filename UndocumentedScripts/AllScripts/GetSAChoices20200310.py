from dsa_util import *
from subprocess import Popen

tables = []
#tables.append(DSTable('PJT', r'T:\TIM_3.1\MinPJTvsMinIMP\MinPJT\_trip_2.dat', '\t'))
#tables.append(DSTable('IMP', r'T:\TIM_3.1\MinPJTvsMinIMP\MinImp\_trip_2.dat', '\t'))
tables.append(DSTable('545hr', r'T:\TIM_3.1\VOT11Skim\scenario\Output\_trip_2.dat', '\t'))
tables = ReadTables(tables)

output = {}
for label in tables:
    transit = tables[label].query('mode == 6')
    output[label] = transit[['otaz', 'trexpfac']].groupby('otaz').sum()['trexpfac']

outfile = r'D:\TIM3\OriginStopAreas545perHour.csv'
pd.DataFrame(output).to_csv(outfile)
Popen(outfile, shell = True)