import pandas as pd

base_tour_file = r'R:\Model_Development\TIM_3.1\scenario\Output\Output_Base_0303\_tour_2.dat'
test_tour_file = r'B:\model_development\TIM_3.1_Github - Copy\scenario\output\_tour_2.dat'

base = pd.read_csv(base_tour_file, '\t')
test = pd.read_csv(test_tour_file, '\t')

print('Base: {}'.format(base.query('tdtaz >= 50000 and totaz < 50000')['toexpfac'].sum()))
print('Test: {}'.format(test.query('tdtaz >= 50000 and totaz < 50000')['toexpfac'].sum()))