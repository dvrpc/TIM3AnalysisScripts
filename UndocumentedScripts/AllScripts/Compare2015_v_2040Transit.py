from dsa_util import *

tables = []
tables.append(DSTable('2015', r'T:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\_trip_2.dat', '\t'))
tables.append(DSTable('2040', r'B:\model_development\TIM_3.1_2040\scenario\Output\_trip_2.dat', '\t'))
tables = ReadTables(tables)

print('2015: {}'.format(tables['2015'].query('mode == 6')['trexpfac'].sum()))
print('2040: {}'.format(tables['2040'].query('mode == 6')['trexpfac'].sum()))