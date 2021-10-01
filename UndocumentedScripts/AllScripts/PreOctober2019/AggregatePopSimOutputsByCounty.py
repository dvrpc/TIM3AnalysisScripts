import pandas as pd
import os
from subprocess import Popen

#Read in input files
#base_path = r'Y:\TIM_3.1\DVRPC_ABM_VISUM18patch\scenario'
base_path = r'R:\Model_Development\TIM_3.1\scenario'
#hh_daysim_file = os.path.join(base_path, 'inputs', '_DVRPC_hrec.dat')
#per_daysim_file = os.path.join(base_path, 'inputs', '_DVRPC_prec.dat')
hh_daysim_file = os.path.join(base_path, 'Output', '_household_2.dat')
per_daysim_file = os.path.join(base_path, 'Output', '_person_2.dat')
#hh_survey_file = os.path.join(base_path, 'DaySimSummaries', 'data', 'dvrpc_hrecx4.dat')
#per_survey_file = os.path.join(base_path, 'DaySimSummaries', 'data', 'dvrpc_precx5.dat')
county_pop_file = r'D:\TIM3\HHPopEmpByCounty.csv'
taz2county_file = r'D:\TIM3\taz2county.csv'
outfile = os.path.join(base_path, 'inputs', 'SynthPopEmpByCounty.xlsx')

county_data = pd.read_csv(county_pop_file, index_col = 0)
county_data.loc['Rest of PA'] = county_data.loc['Berks'] + county_data.loc['Lancaster'] + county_data.loc['Lehigh'] + county_data.loc['Northampton']
county_data.loc['Rest of NJ'] = county_data.loc['Warren'] + county_data.loc['Hunterdon'] + county_data.loc['Somerset'] + county_data.loc['Middlesex'] + county_data.loc['Monmouth'] + county_data.loc['Ocean'] + county_data.loc['Atlantic'] + county_data.loc['Cape May'] + county_data.loc['Cumberland'] + county_data.loc['Salem']
county_data.loc['Rest of Outer Counties'] = county_data.loc['New Castle'] + county_data.loc['Cecil']

hh_daysim = pd.read_csv(hh_daysim_file, delimiter = '\t')
per_daysim = pd.read_csv(per_daysim_file, delimiter = '\t')
#hh_survey = pd.read_csv(hh_survey_file, delimiter = ',')
#per_survey = pd.read_csv(per_survey_file, delimiter = ' ')
taz2county = pd.read_csv(taz2county_file, index_col = 0)['County']

#Get household county
hh_daysim['County'] = hh_daysim['hhtaz'].map(taz2county)
#hh_survey['County'] = hh_survey['hhtaz'].map(taz2county)

#Aggregate households by county
hh_by_county_daysim = hh_daysim[['County', 'hhexpfac']].groupby('County').sum()['hhexpfac']
#hh_by_county_survey = hh_survey[['County', 'hhexpfac']].groupby('County').sum()['hhexpfac']

hh_by_county = pd.DataFrame({'Target': county_data['Households'], 'DaySim': hh_by_county_daysim}).dropna()
hh_by_county['Error'] = hh_by_county['DaySim'] - hh_by_county['Target']
hh_by_county['% Error'] = hh_by_county['Error'] / hh_by_county['Target']

#Merge household and person files
hhper_daysim = hh_daysim.merge(per_daysim, on = 'hhno')
#hhper_survey = hh_survey.merge(per_survey, on = 'hhno')

#Aggregate population by county
per_by_county_daysim = hhper_daysim[['County', 'psexpfac']].groupby('County').sum()['psexpfac']
#per_by_county_survey = hhper_survey[['County', 'psexpfac']].groupby('County').sum()['psexpfac']

per_by_county = pd.DataFrame({'Target': county_data['Population'], 'DaySim': per_by_county_daysim}).dropna()
per_by_county['Error'] = per_by_county['DaySim'] - per_by_county['Target']
per_by_county['% Error'] = per_by_county['Error'] / per_by_county['Target']

per_daysim['wcounty'] = per_daysim['pwtaz'].map(taz2county)
emp_by_county_daysim = per_daysim[['wcounty', 'psexpfac']].groupby('wcounty').sum()['psexpfac']
emp_by_county = pd.DataFrame({'Target': county_data['Employment'], 'DaySim': emp_by_county_daysim}).dropna()
emp_by_county['Error'] = emp_by_county['DaySim'] - emp_by_county['Target']
emp_by_county['% Error'] = emp_by_county['Error'] / emp_by_county['Target']

#Combine output
output = pd.Panel({'Households': hh_by_county, 'Population': per_by_county, 'Employment': emp_by_county})
output.to_excel(outfile)
Popen(outfile, shell = True)

print('Go')