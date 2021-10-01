import pandas as pd
import numpy as np

hh_file_survey = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_household_2.dat'
per_file_survey = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_person_2.dat'
hh_file_daysim = r'Y:\TIM_3.1\Temp\scenario\Output\_household_2.dat'
per_file_daysim = r'Y:\TIM_3.1\Temp\scenario\Output\_person_2.dat'

hh_survey = pd.read_csv(hh_file_survey, '\t')
per_survey = pd.read_csv(per_file_survey, '\t')
hh_daysim = pd.read_csv(hh_file_daysim, '\t')
per_daysim = pd.read_csv(per_file_daysim, '\t')

students = {}
students['survey'] = 