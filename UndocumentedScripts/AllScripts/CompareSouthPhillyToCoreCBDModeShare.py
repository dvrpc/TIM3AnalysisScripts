import pandas as pd
import numpy as np
import os

def pivot(table, row, col, weight):
    return table[[row, col, weight]].groupby([row, col]).sum()[weight].reset_index().pivot(row, col, weight).fillna(0)

def reclassify_workbased(args):
    parent = args[0]
    pdpurp = args[1]
    if parent > 0:
        return 'WB'
    else:
        return pdpurp

def identify_and_reclassify_workbased(tour):
    tour['args'] = list(zip(tour['parent'], tour['pdpurp']))
    tour['pdpurp'] = tour['args'].apply(reclassify_workbased)

def get_perdata(tour, fp):
    per = pd.read_csv(fp.replace('tour', 'person'), '\t')
    tour = per.merge(tour, on = ['hhno', 'pno'])

parcel_file = r'R:\Model_Development\TIM_3.1\scenario\inputs\parcels_buffered.dat'
parcel = pd.read_csv(parcel_file, ' ', index_col = 0)
parcel['CoreCBD'] = ((parcel['hh_1'] + parcel['emptot_1']) > 20000)

survey_file = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_tour_2.dat'
base_file = r'R:\Model_Development\TIM_3.1\scenario\Output\Output_Base_0303\_tour_2.dat'
test_file = r'R:\Model_Development\TIM_3.1\scenario\Output\_tour_2.dat'

print('Reading')
survey = pd.read_csv(survey_file, '\t')
base = pd.read_csv(base_file, '\t')
test = pd.read_csv(test_file, '\t')

#get_perdata(survey, survey_file)
#get_perdata(base, base_file)
#get_perdata(test, test_file)

print('Processing')
survey['tdCoreCBD'] = survey['tdpcl'].map(parcel['CoreCBD'])
base['tdCoreCBD'] = base['tdpcl'].map(parcel['CoreCBD'])
test['tdCoreCBD'] = test['tdpcl'].map(parcel['CoreCBD'])

qry = 'totaz >= 800 and tdtaz < 1000 and tdCoreCBD == True'
survey = survey.query(qry)
base = base.query(qry)
test = test.query(qry)

identify_and_reclassify_workbased(survey)
identify_and_reclassify_workbased(base)
identify_and_reclassify_workbased(test)

survey_trips = pivot(survey, 'tmodetp', 'pdpurp', 'toexpfac')
base_trips = pivot(base, 'tmodetp', 'pdpurp', 'toexpfac')
test_trips = pivot(test, 'tmodetp', 'pdpurp', 'toexpfac')

print('Writing')
outfile = r'D:\TIM3\SouthPhillyToCoreCBDTourFlow_Raw.xlsx'
writer = pd.ExcelWriter(outfile)
survey_trips.to_excel(writer, 'Survey')
base_trips.to_excel(writer, 'Base')
test_trips.to_excel(writer, 'Test')
writer.close()
print('Done')

#print('Survey')
#print(survey_trips)
#print('\n')

#print('Base')
#print(base_trips)
#print('\n')

#print('Test')
#print(test_trips)