import pandas as pd

base_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\Output\iter3\_tour_2.dat'
test_file = r'D:\TIM3.1\CenterCityScreenlineCalibration\scenario\Output\_tour_2.dat'

print('Reading Base')
base = pd.read_csv(base_file, '\t')
print('Reading Test')
test = pd.read_csv(test_file, '\t')

qry = 'pdpurp == 1 and totaz > 56000 and totaz < 56500 and tdtaz < 4000'

print('Base: {}'.format(base.query(qry)['toexpfac'].sum()))
print('Test: {}'.format(test.query(qry)['toexpfac'].sum()))