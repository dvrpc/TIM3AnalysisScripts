import pandas as pd
import numpy as np

hh_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\Output\0323\_household_2.dat'
per_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\Output\0323\_person_2.dat'

hh = pd.read_csv(hh_file, '\t').query('hhtaz < 50000')
per = pd.read_csv(per_file, '\t')

perdata = per.merge(hh, on = 'hhno', how = 'left')
perdata['work'] = ((perdata['pwtyp'] > 0) & (perdata['pwtaz'] != 0)).astype(int)
perdata['stud'] = ((perdata['pptyp'] >= 5) & (perdata['pptyp'] <= 7) & perdata['pstaz'] != 0).astype(int)

workers = perdata.query('work == 1 and pwaudist >= 0')
students = perdata.query('stud == 1 and psaudist >= 0')

print(np.average(workers['pwaudist'], weights = workers['psexpfac']))
print(np.average(students['psaudist'], weights = students['psexpfac']))

print('Go')