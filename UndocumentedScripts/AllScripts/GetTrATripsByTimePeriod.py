from dsa_util import *
from subprocess import Popen

def fix_time(t):
    hr = t // 100
    min = t % 100
    return (60*hr + min) % 1440

def classify_time_period(args):
    half = args[0]
    if half == 1:
        t = args[2]
    elif half == 2:
        t = args[1]
    if t < 360:
        return 'NT'
    elif t < 600:
        return 'AM'
    elif t < 900:
        return 'MD'
    elif t < 1140:
        return 'PM'
    else:
        return 'NT'

base_path = r'T:\TIM_3.1\DVRPC_ABM_Testing\scenario\output\0623'
need_to_fix_time = False
tables = []
tables.append(DSTable('household', os.path.join(base_path, '_household_2.dat'), '\t'))
tables.append(DSTable('tour', os.path.join(base_path, '_tour_2.dat'), '\t'))
tables.append(DSTable('trip', os.path.join(base_path, '_trip_2.dat'), '\t'))
tables = ReadTables(tables)

if need_to_fix_time:
    tables['trip']['deptm'] = tables['trip']['deptm'].apply(fix_time)
    tables['trip']['arrtm'] = tables['trip']['arrtm'].apply(fix_time)

tourtrip = tables['tour'].merge(tables['trip'], on = ['hhno', 'pno', 'day', 'tour'])
tourtrip['htaz'] = tourtrip['hhno'].map(tables['household'].set_index('hhno')['hhtaz'])
dt_t = tourtrip.query('htaz < 50000 and mode == 6')
dt_t['args'] = list(zip(dt_t['half'], dt_t['deptm'], dt_t['arrtm']))
dt_t['TOD'] = dt_t['args'].apply(classify_time_period)

gb_tod = dt_t[['TOD', 'trexpfac']].groupby(['TOD']).sum()['trexpfac']
outfile = os.path.join(base_path, 'TransitTripsByTOD.csv')
gb_tod.to_csv(outfile)
Popen(outfile, shell = True)