import pandas as pd

hh_file = r'Y:\TIM_3.1\DVRPC_ABM_Template\scenario\Output\_household_2.dat'
per_file = r'Y:\TIM_3.1\DVRPC_ABM_Template\scenario\Output\_person_2.dat'

hh = pd.read_csv(hh_file, '\t')
per = pd.read_csv(per_file, '\t')
hhper = hh.merge(per, on = 'hhno')
workers = hhper.query('pwtaz > 0')
workers_by_zone = workers.groupby('hhtaz').sum()['psexpfac']
workers_by_zone.to_csv(r'D:\TIM3\workers_by_zone.csv')

print('Done')