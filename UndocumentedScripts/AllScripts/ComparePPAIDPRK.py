import pandas as pd
import numpy as np
import os

survey_hh_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\DaySimSummaries\data\dvrpc_hrecx4.dat'
model_hh_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\Output\_household_2.dat'

survey_per_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\DaySimSummaries\data\dvrpc_precx5.dat'
model_per_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\Output\_person_2.dat'

qry = 'hhtaz >= 1400 and hhtaz < 1800 and pwtaz > 0 and pwtaz < 200'

print('Reading Survey Data')
survey_hh = pd.read_csv(survey_hh_file, ',')
survey_per = pd.read_csv(survey_per_file, ' ')
survey_hhper = survey_hh.merge(survey_per, on = 'hhno').query(qry)

print('Reading Modeled Data')
model_hh = pd.read_csv(model_hh_file, '\t')
model_per = pd.read_csv(model_per_file, '\t')
model_hhper = model_hh.merge(model_per, on = 'hhno').query(qry)

print('Survey: {0}/{1}'.format((survey_hhper['ppaidprk']*survey_hhper['psexpfac']).sum(), survey_hhper['psexpfac'].sum()))
print('Model:  {0}/{1}'.format((model_hhper['ppaidprk']*model_hhper['psexpfac']).sum(), model_hhper['psexpfac'].sum()))