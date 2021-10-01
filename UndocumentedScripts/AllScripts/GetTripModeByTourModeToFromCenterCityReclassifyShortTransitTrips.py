#from dsa_util import *
import pandas as pd
import numpy as np
import os
from subprocess import Popen

survey_path = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output'
survey_tables = {}
survey_tables['tour'] = pd.read_csv(os.path.join(survey_path, '_tour_2.dat'), '\t')
survey_tables['trip'] = pd.read_csv(os.path.join(survey_path, '_trip_2.dat'), '\t')
#survey_tables.append(DSTable('tour', os.path.join(survey_path, '_tour_2.dat'), '\t'))
#survey_tables.append(DSTable('trip', os.path.join(survey_path, '_trip_2.dat'), '\t'))
#survey_tables = ReadTables(survey_tables)

#base_path = r'T:\TIM_3.1\DVRPC_ABM_Testing\scenario\output'
#base_path = r'Y:\TIM_3.1\Temp\scenario\Output'
#base_path = r'D:\TIM3.1\CenterCityScreenlineCalibration\scenario\Output'
#base_path = r'D:\TIM3.1\TestDA2ndHalfFromYoshiTemp\scenario\Output'
#base_path = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\Output'
#base_path = r'R:\Model_Development\TIM_3.1\scenario\Output'
#base_path = r'B:\model_development\TIM_3.1_Github - Copy\scenario\output\Time Utility_decrease'
#base_path = r'D:\TIM3.1\200630_NoTripDestParkingSensitivity\scenario\Output\10%'
base_path = r'B:\model_development\TIM_3.1_Github - Copy\scenario\output\Coeff_103'
tables = {}
tables['hh'] = pd.read_csv(os.path.join(base_path, '_household_2.dat'), '\t')
tables['tour'] = pd.read_csv(os.path.join(base_path, '_tour_2.dat'), '\t')
tables['trip'] = pd.read_csv(os.path.join(base_path, '_trip_2.dat'), '\t')
#tables.append(DSTable('hh', os.path.join(base_path, '_household_2.dat'), '\t'))
#tables.append(DSTable('tour', os.path.join(base_path, '_tour_2.dat'), '\t'))
#tables.append(DSTable('trip', os.path.join(base_path, '_trip_2.dat'), '\t'))
#tables = ReadTables(tables)

hh2taz = tables['hh'].set_index('hhno')['hhtaz']

tables['tour']['hhtaz'] = tables['tour']['hhno'].map(hh2taz)
tables['trip']['hhtaz'] = tables['trip']['hhno'].map(hh2taz)

tables['tour'] = tables['tour'].query('hhtaz < 50000')
tables['trip'] = tables['trip'].query('hhtaz < 50000')

tables['trip']['mode'] = np.where((tables['trip']['mode'] == 6) & (tables['trip']['travdist'] <= 0.5), 1, tables['trip']['mode'])

#tourtrip = tables['tour'].merge(tables['trip'], on = ['hhno', 'pno', 'day', 'tour'])
#in_cc = tourtrip.query('otaz >= 200 and dtaz < 200')
#out_cc = tourtrip.query('otaz < 200 and dtaz >= 200')

def pivot_by_mode(data):
    return data[['tmodetp', 'mode', 'trexpfac']].groupby(['tmodetp', 'mode']).sum()['trexpfac'].reset_index().pivot('tmodetp', 'mode', 'trexpfac').fillna(0)

def process_data(tables):
    tour_fields = ['hhno', 'pno', 'day', 'tour', 'pdpurp', 'tmodetp']
    trip_fields = ['hhno', 'pno', 'day', 'tour', 'mode', 'otaz', 'dtaz', 'trexpfac']
    tourtrip = tables['tour'][tour_fields].merge(tables['trip'][trip_fields], on = ['hhno', 'pno', 'day', 'tour'])
    in_cc = tourtrip.query('otaz >= 200 and dtaz < 200')
    out_cc = tourtrip.query('otaz < 200 and dtaz >= 200')

    outtables = {}
    outtables['in'] = pivot_by_mode(in_cc)
    outtables['out'] = pivot_by_mode(out_cc)
    return outtables

daysim = process_data(tables)
survey = process_data(survey_tables)

outfile = os.path.join(r'D:\TIM3\ToFromCCModeTrips_Bowser_2MarCoef103_ShortTransitReclassified_Raw.xlsx')
writer = pd.ExcelWriter(outfile)
survey['in'].to_excel(writer, 'Inbound (Survey)')
daysim['in'].to_excel(writer, 'Inbound (DaySim)')
survey['out'].to_excel(writer, 'Outbound (Survey)')
daysim['out'].to_excel(writer, 'Outbound (DaySim)')
writer.close()

Popen(outfile, shell = True)