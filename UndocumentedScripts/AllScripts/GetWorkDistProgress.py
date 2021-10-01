from dsa_util import *
import os
from subprocess import Popen
from collections import OrderedDict

tables = []
tables.append(DSTable('0 Iter',  r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\NoShadowPrice\_person_2.dat', '\t'))
tables.append(DSTable('4 Iter',  r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\4Iters\_person_2.dat',  '\t'))
tables.append(DSTable('8 Iter',  r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\8Iters\_person_2.dat',  '\t'))
tables.append(DSTable('12 Iter', r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\12Iters\_person_2.dat', '\t'))
tables.append(DSTable('16 Iter', r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\16Iters\_person_2.dat', '\t'))
tables = ReadTables(tables)

def get_grouping(tables, grouper, weight, qry = None):
    output = pd.DataFrame()
    for name in tables:
        if qry is None:
            output[name] = tables[name][[grouper, 'psexpfac']].groupby(grouper).sum()['psexpfac']
        else:
            output[name] = tables[name].query(qry)[[grouper, 'psexpfac']].groupby(grouper).sum()['psexpfac']
    return output

#emp_by_taz = get_grouping(tables, 'pwtaz', 'psexpfac', 'pwtaz > 0')
#emp_by_maz = get_grouping(tables, 'pwpcl', 'psepxfac', 'pwtaz > 0')

#outfile = r'D:\TIM3\ShadowPricingEffect\GroupedWorkLocations.xlsx'
#writer = pd.ExcelWriter(outfile)
#emp_by_taz.to_excel(writer, 'TAZ')
#emp_by_maz.to_excel(writer, 'MAZ')
#writer.close()

atls = pd.Series(np.zeros(5), range(0, 17, 4))
for i in range(0, 17, 4):
    workers = tables['%d Iter'%(i)][['pwtaz', 'pwaudist', 'psexpfac']].query('pwtaz > 0')
    atls[i] = np.average(workers['pwaudist'], weights = workers['psexpfac'])

print(atls)


print('Completed')