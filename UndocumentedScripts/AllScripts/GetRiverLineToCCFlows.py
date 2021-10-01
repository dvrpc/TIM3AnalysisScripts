import pandas as pd
import numpy as np

survey_file = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_tour_2.dat'
ds_file = r'D:\TIM3.1\CalibrationJune2021\scenario\Output\0712Base\_tour_2.dat'
taz2cpa_file = r'D:\ref\taz2cpa.csv'

survey = pd.read_csv(survey_file, '\t')
ds = pd.read_csv(ds_file, '\t')
taz2cpa = pd.read_csv(taz2cpa_file, index_col = 0)['CPA']

survey['tocpa'] = survey['totaz'].map(taz2cpa)
survey['tdcpa'] = survey['tdtaz'].map(taz2cpa)
ds['tocpa'] = ds['totaz'].map(taz2cpa)
ds['tdcpa'] = ds['tdtaz'].map(taz2cpa)

qry = 'tdcpa == 701 and tocpa == 103 and (tmodetp == 6 or tmodetp == 7)'

print('\n701')
print('Survey: {}'.format(survey.query(qry)['toexpfac'].sum()))
print('DaySim: {}'.format(ds.query(qry)['toexpfac'].sum()))

qry = qry.replace('701', '801')

print('\n801')
print('Survey: {}'.format(survey.query(qry)['toexpfac'].sum()))
print('DaySim: {}'.format(ds.query(qry)['toexpfac'].sum()))

print('Go')