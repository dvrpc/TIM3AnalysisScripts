from dsa_util import *

tables = []
tables.append(DSTable('hh0', r'Y:\TIM_3.1\TIM31_HigherTransitCoefficients\scenario\Output\_household_2.dat', '\t'))
tables.append(DSTable('ps0', r'Y:\TIM_3.1\TIM31_HigherTransitCoefficients\scenario\Output\_person_2.dat', '\t'))
tables.append(DSTable('hh1', r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\4Iters\_household_2.dat', '\t'))
tables.append(DSTable('ps1', r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\4Iters\_person_2.dat', '\t'))
tables = ReadTables(tables)


#Queries
res_in_phila = 'hhtaz < 4000'
work_in_phila = 'pwtaz < 4000'
work_in_ac = 'pwtaz == 56002'

hhper0 = tables['hh0'].merge(tables['ps0'], on = 'hhno').query(res_in_phila)
hhper1 = tables['hh1'].merge(tables['ps1'], on = 'hhno').query(res_in_phila)

hhper0['id'] = 100*hhper0['hhno'] + hhper0['pno']
hhper1['id'] = 100*hhper1['hhno'] + hhper1['pno']

phila2phila_0 = hhper0.query(work_in_phila)
phila2ac_1 = hhper1.query(work_in_ac)

phila2phila_hh = list(phila2phila_0['id'])
phila2ac_hh = list(phila2ac_1['id'])

phila_ac_shift_hh = list(set(phila2phila_hh) & set(phila2ac_hh))
shift0 = hhper0.query('id in @phila_ac_shift_hh')
shift1 = hhper1.query('id in @phila_ac_shift_hh')

person_of_interest = int(shift0.query('hhtaz == 821 and pwtaz == 44').iloc[0]['id'])
info0 = hhper0.query('id == @person_of_interest')
info1 = hhper1.query('id == @person_of_interest')

pd.set_option('display.max_columns', None)
pd.options.display.max_seq_items = None
fields_to_print = ['hhno', 'pno', 'hhparcel', 'hhtaz', 'hhincome', 'pptyp', 'pagey', 'pgend', 'pwtyp', 'pwpcl', 'pwtaz', 'pwaudist']
print('No Shadow Pricing:')
print(info0[fields_to_print])
print('\nWith Shadow Pricing:')
print(info1[fields_to_print])