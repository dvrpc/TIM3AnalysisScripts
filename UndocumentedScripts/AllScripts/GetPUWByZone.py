from dsa_util import *
import os
from subprocess import Popen

tables = []
tables.append(DSTable('Before',  r'T:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\_person_2.dat', '\t'))
tables.append(DSTable('After',  r'T:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\Backup\_person_2.dat',  '\t'))
tables = ReadTables(tables)

def get_grouping(tables, grouper, weight, qry = None):
    output = pd.DataFrame()
    for name in tables:
        if qry is None:
            output[name] = tables[name][[grouper, 'psexpfac']].groupby(grouper).sum()['psexpfac']
        else:
            output[name] = tables[name].query(qry)[[grouper, 'psexpfac']].groupby(grouper).sum()['psexpfac']
    return output

emp_by_taz = get_grouping(tables, 'pwtaz', 'psexpfac', 'pwtaz > 0')
emp_by_maz = get_grouping(tables, 'pwpcl', 'psepxfac', 'pwtaz > 0')

outfile = r'D:\TIM3\ShadowPricingCheck2040\GroupedWorkLocations.xlsx'
writer = pd.ExcelWriter(outfile)
emp_by_taz.to_excel(writer, 'TAZ')
emp_by_maz.to_excel(writer, 'MAZ')
writer.close()

print('Completed')