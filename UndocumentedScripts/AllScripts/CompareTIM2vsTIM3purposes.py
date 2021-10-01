from dsa_util import *

base_path = r'B:\model_development\TIM_3.1\scenario\Output'
names = ['hh', 'per', 'tour', 'trip']
fps = [os.path.join(base_path, '_household_2.dat'),
       os.path.join(base_path, '_person_2.dat'),
       os.path.join(base_path, '_tour_2.dat'),
       os.path.join(base_path, '_trip_2.dat')]
tables = ReadTables(names, fps, 4*['\t'])
tables['trip']['tim2purp'] = classify_tim2_purposes(tables['per'], tables['trip'])

tourtrip = tables['tour'][['hhno', 'pno', 'day', 'tour', 'pdpurp']].merge(tables['trip'][['hhno', 'pno', 'day', 'tour', 'tim2purp', 'trexpfac']], on = ['hhno', 'pno', 'day', 'tour'])
purpmtx = tourtrip[['pdpurp', 'tim2purp', 'trexpfac']].groupby(['pdpurp', 'tim2purp']).sum()['trexpfac'].reset_index().pivot('pdpurp', 'tim2purp', 'trexpfac').fillna(0)

purpmtx.to_csv(r'D:\ref\tim2purp_to_tim3purp_survey.csv')

print('Go')