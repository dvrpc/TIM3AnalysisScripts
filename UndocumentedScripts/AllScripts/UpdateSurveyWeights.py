from dsa_util import *

base_path = r'T:\TIM_3.1\200220_FewerFarAwayWorkplaceChoices\scenario\DaySimSummaries\data'
tables = []
tables.append(DSTable('hh', os.path.join(base_path, 'dvrpc_hrecx4.dat'), ','))
tables.append(DSTable('hd', os.path.join(base_path, 'dvrpc_hdayx4.dat'), ' '))
tables.append(DSTable('ps', os.path.join(base_path, 'dvrpc_precx5.dat'), ' '))
tables.append(DSTable('pd', os.path.join(base_path, 'dvrpc_pdayx5.dat'), ' '))
tables.append(DSTable('to', os.path.join(base_path, 'dvrpc_tourx5.dat'), ' '))
tables.append(DSTable('tr', os.path.join(base_path, 'dvrpc_tripx5.dat'), ' '))
print('Reading Files')
tables = ReadTables(tables)

outfiles = {'hh': os.path.join(base_path, 'dvrpc_hrecx6.dat'),
            'hd': os.path.join(base_path, 'dvrpc_hdayx6.dat'),
            'ps': os.path.join(base_path, 'dvrpc_precx6.dat'),
            'pd': os.path.join(base_path, 'dvrpc_pdayx6.dat'),
            'to': os.path.join(base_path, 'dvrpc_tourx6.dat'),
            'tr': os.path.join(base_path, 'dvrpc_tripx6.dat')}

hh2weight = tables['hh'].set_index('hhno')['hhexpfac'] #For mapping household ID to expansion factor

for label in tables:
    print('Updating ' + label)
    weight = label + 'expfac'
    tables[label][weight] = tables[label]['hhno'].map(hh2weight)
    tables[label].to_csv(outfiles[label], sep = '\t', index = False)

print('Done')