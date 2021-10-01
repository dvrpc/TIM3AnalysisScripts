from dsa_util import *
import os
from subprocess import Popen

order = [42100, 42101, 42045, 42029, 42091, 42017, 34021, 34005, 34007, 34015, 42071, 42011, 42077, 42095,
         34041, 34019, 34035, 34023, 34025, 34029, 34001, 34009, 34011, 34033, 10003, 24015]

base_path = r'T:\TIM_3.1\Sensitivity_Emp\scenario\Output'
tables = []
tables.append(DSTable('hh', os.path.join(base_path, '_household_2.dat'), '\t'))
tables.append(DSTable('ps', os.path.join(base_path, '_person_2.dat'),    '\t'))
tables = ReadTables(tables)
workers = tables['hh'].merge(tables['ps']).query('pwtyp > 0')

taz2fips_file = r'D:\ref\taz2fips.csv'
taz2county = pd.read_csv(taz2fips_file, index_col = 0)['STATE_COUNTY_ID']
for i in range(200):
    taz2county[i] = 42100

workers['hcounty'] = workers['hhtaz'].map(taz2county)
workers['wcounty'] = workers['pwtaz'].map(taz2county)

county_flow = workers[['hcounty', 'wcounty', 'psexpfac']].groupby(['hcounty', 'wcounty']).sum().reset_index().pivot('hcounty', 'wcounty', 'psexpfac').fillna(0).loc[order, order]

outfile = os.path.join(base_path, 'FullCountyFlow.csv')
county_flow.to_csv(outfile)
Popen(outfile, shell = True)

print('Go')