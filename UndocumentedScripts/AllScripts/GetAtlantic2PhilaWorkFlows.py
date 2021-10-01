import pandas as pd

base_hh_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\Output\iter3\_household_2.dat'
base_per_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\Output\iter3\_person_2.dat'
test_hh_file = r'D:\TIM3.1\CenterCityScreenlineCalibration\scenario\Output\_household_2.dat'
test_per_file = r'D:\TIM3.1\CenterCityScreenlineCalibration\scenario\Output\_person_2.dat'

print('Reading Base')
base_hh = pd.read_csv(base_hh_file, '\t')
base_per = pd.read_csv(base_per_file, '\t')
print('Reading Test')
test_hh = pd.read_csv(test_hh_file, '\t')
test_per = pd.read_csv(test_per_file, '\t')

base = base_hh.merge(base_per, on = 'hhno')
test = test_hh.merge(test_per, on = 'hhno')

qry = 'hhtaz > 56000 and hhtaz < 56500 and pwtaz > 0 and pwtaz < 4000'

print('Base: {}'.format(base.query(qry)['psexpfac'].sum()))
print('Test: {}'.format(test.query(qry)['psexpfac'].sum()))