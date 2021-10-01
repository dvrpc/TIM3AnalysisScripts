from dsa_util import *

base_path = r'T:\TIM_3.1\DVRPC_ABM_Testing\scenario\output'
test_path = r'B:\model_development\TIM_3.1_Testing\scenario\Output'
tables = []
tables.append(DSTable('tour0', os.path.join(base_path, '_tour_2.dat'), '\t'))
tables.append(DSTable('trip0', os.path.join(base_path, '_trip_2.dat'), '\t'))
tables.append(DSTable('tour1', os.path.join(test_path, '_tour_2.dat'), '\t'))
tables.append(DSTable('trip1', os.path.join(test_path, '_trip_2.dat'), '\t'))
tables = ReadTables(tables)

print('Base: {}'.format(tables['trip0']['trexpfac'].sum() / tables['tour0']['toexpfac'].sum()))
print('Test: {}'.format(tables['trip1']['trexpfac'].sum() / tables['tour1']['toexpfac'].sum()))