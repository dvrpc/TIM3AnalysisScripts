'''
This script compares the number of workers from households with incomes over and under 100k going to and from Center City for work.
'''
import pandas as pd
import numpy as np

files = {}
files['parcel'] = r'D:\TIM3.1\CenterCityScreenlineCalibration\scenario\inputs\parcels_buffered.dat'
files['survey_hh'] = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_household_2.dat'
files['survey_per'] = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_person_2.dat'
files['daysim_hh'] = r'Y:\TIM_3.1\WorkLocCoreCBD\scenario\Output\_household_2.dat'
files['daysim_per'] = r'Y:\TIM_3.1\WorkLocCoreCBD\scenario\Output\_person_2.dat'
#files['daysim_hh'] = r'D:\TIM3.1\CenterCityScreenlineCalibration\scenario\Output\_household_2.dat'
#files['daysim_per'] = r'D:\TIM3.1\CenterCityScreenlineCalibration\scenario\Output\_person_2.dat'

tables = {}
for name in files:
    print('Reading ' + name)
    if name == 'parcel':
        tables[name] = pd.read_csv(files[name], ' ')
    else:
        tables[name] = pd.read_csv(files[name], '\t')

print('Merging')
qry = 'pwtaz > 0 and hhtaz < 50000 and hhincome >= 100000'
survey_workers = tables['survey_hh'].merge(tables['survey_per'], on = 'hhno').query(qry)
daysim_workers = tables['daysim_hh'].merge(tables['daysim_per'], on = 'hhno').query(qry)

print('Identifying CBD Parcels')
tables['parcel']['cbd'] = ((tables['parcel']['hh_1'] + tables['parcel']['emptot_1']) >= 20000)
survey_workers['hhcbd'] = survey_workers['hhparcel'].map(tables['parcel'].set_index('parcelid')['cbd'])
daysim_workers['hhcbd'] = daysim_workers['hhparcel'].map(tables['parcel'].set_index('parcelid')['cbd'])
survey_workers['pwcbd'] = survey_workers['pwpcl'].map(tables['parcel'].set_index('parcelid')['cbd'])
daysim_workers['pwcbd'] = daysim_workers['pwpcl'].map(tables['parcel'].set_index('parcelid')['cbd'])

print('Comparing CBD Work Locations')
grouped = {}
grouped['survey'] = survey_workers.groupby('pwcbd').sum()['psexpfac']
grouped['daysim'] = daysim_workers.groupby('pwcbd').sum()['psexpfac']
grouped = pd.DataFrame(grouped)
print(grouped)

print('\n')
print(survey_workers.groupby(['hhcbd', 'pwcbd']).sum()['psexpfac'].reset_index().pivot('hhcbd', 'pwcbd', 'psexpfac'))
print('\n')
print(daysim_workers.groupby(['hhcbd', 'pwcbd']).sum()['psexpfac'].reset_index().pivot('hhcbd', 'pwcbd', 'psexpfac'))

print('Done')