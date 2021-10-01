import pandas as pd
import os
from subprocess import Popen

survey_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\DaySimSummaries\data\dvrpc_hrecx4.dat'
survey = pd.read_csv(survey_file, ',')
daysim_file = r'B:\model_development\TIM_3.1\scenario\Output\_household_2.dat'
daysim = pd.read_csv(daysim_file, '\t')

taz2cpa_file = r'D:\ref\taz2cpa.csv'
taz2cpa = pd.read_csv(taz2cpa_file, index_col = 0)['CPA']

by_cpa = False
for_subway_tazs = True

def get_hhveh_by_cpa(hh):
    global taz2cpa
    hh['hhcpa'] = hh['hhtaz'].map(taz2cpa)
    return hh[['hhvehs', 'hhcpa', 'hhexpfac']].groupby(['hhvehs', 'hhcpa']).sum()['hhexpfac'].reset_index().pivot('hhcpa', 'hhvehs', 'hhexpfac')




if by_cpa:
    outfile = r'D:\TIM3\HHVEHSBYCOUNTYPLANNINGAREA.xlsx'

    

    pivot_survey = get_hhveh_by_cpa(survey)
    pivot_daysim = get_hhveh_by_cpa(daysim)

    writer = pd.ExcelWriter(outfile)
    pivot_survey.to_excel(writer, 'raw')
    pivot_daysim.to_excel(writer, 'raw', startcol = 20)
    writer.close()
    Popen(outfile, shell = True)

if for_subway_tazs:
    subway_taz_file = r'D:\ref\SubwayTAZs.txt'
    f = open(subway_taz_file)
    lines = f.read().split()
    f.close()
    subway_tazs = [int(line) for line in lines]
    outfile = r'D:\TIM3\HHVehsInSubwayTAZs.csv'

    def get_hhveh_for_subwaytaz(hh):
        global subway_tazs

        return hh[['hhtaz', 'hhvehs', 'hhexpfac']].query('hhtaz in @subway_tazs').groupby(['hhvehs']).sum()['hhexpfac']

    output = {}
    output['survey'] = get_hhveh_for_subwaytaz(survey)
    output['daysim'] = get_hhveh_for_subwaytaz(daysim)

    pd.DataFrame(output).to_csv(outfile)
    Popen(outfile, shell = True)

#if for_subway_tazs_wrk:
#    subway_taz_file = r'D:\ref\SubwayTAZs.txt'
#    f = open(subway_taz_file)
#    lines = f.read().split()
#    f.close()
#    subway_tazs = [int(line) for line in lines]
#    outfile = r'D:\TIM3\HHVehsInSubwayTAZs.csv'

#    def get_hhveh_for_subwaytaz(hh):
#        global subway_tazs

#        return hh[['hhtaz', 'hhvehs', 'hhexpfac']].query('hhtaz in @subway_tazs').groupby(['hhvehs']).sum()['hhexpfac']

#    output = {}
#    output['survey'] = get_hhveh_for_subwaytaz(survey)
#    output['daysim'] = get_hhveh_for_subwaytaz(daysim)

#    pd.DataFrame(output).to_csv(outfile)
#    Popen(outfile, shell = True)