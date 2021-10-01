import pandas as pd
import numpy as np
import os

parcel_file = r'R:\Model_Development\TIM_3.1\scenario\inputs\parcels_buffered.dat'
parcel = pd.read_csv(parcel_file, ' ', index_col = 0)
parcel['CoreCBD'] = ((parcel['hh_1'] + parcel['emptot_1']) > 20000)

survey_hh_file = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_household_2.dat'
survey_per_file = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_person_2.dat'
survey_tour_file = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_tour_2.dat'

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

#base_path = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\Output'
base_path = r'R:\Model_Development\TIM_3.1\scenario\Output\Output_0315'
#base_path = r'B:\model_development\TIM_3.1_Github - Copy\scenario\output'
#base_path = r'D:\TIM3.1\CalibrationIdesOfMarch2021\scenario\Output'
daysim_hh_file = os.path.join(base_path , '_household_2.dat')
daysim_per_file = os.path.join(base_path , '_person_2.dat')
daysim_tour_file = os.path.join(base_path, '_tour_2.dat')

#def separate_workbased(per, tour):
#    print(tour.shape[0])
#    tour = per.merge(tour, on = ['hhno', 'pno'])
#    #tour['WorkBased'] = (tour['pwpcl'] == tour['topcl'])
#    tour['WorkBased'] = (tour['parent'] > 0)
#    work_based = tour.query('WorkBased == True')
#    not_work_based = tour.query('WorkBased == False')
#    print(work_based.shape[0])
#    print(not_work_based.shape[0])
#    return (work_based, not_work_based)

print('Reading Survey')
survey_hh = pd.read_csv(survey_hh_file, '\t')
survey_per = pd.read_csv(survey_per_file, '\t')
survey_tour = pd.read_csv(survey_tour_file, '\t')

print('Reading DaySim')
daysim_hh = pd.read_csv(daysim_hh_file, '\t')
daysim_per = pd.read_csv(daysim_per_file, '\t')
daysim_tour = pd.read_csv(daysim_tour_file, '\t')

print('Filtering')
survey_tour['hhtaz'] = survey_tour['hhno'].map(survey_hh.set_index('hhno')['hhtaz'])
survey_tour['tdCoreCBD'] = survey_tour['tdpcl'].map(parcel['CoreCBD'])
daysim_tour['hhtaz'] = daysim_tour['hhno'].map(daysim_hh.set_index('hhno')['hhtaz'])
daysim_tour['tdCoreCBD'] = daysim_tour['tdpcl'].map(parcel['CoreCBD'])
qry = 'hhtaz < 50000 and tdCoreCBD == True'
survey_tour = survey_tour.query(qry)
daysim_tour = daysim_tour.query(qry)

print('Separating')
#(survey_workbased, survey_tour) = separate_workbased(survey_per, survey_tour)
#(daysim_workbased, daysim_tour) = separate_workbased(daysim_per, daysim_tour)
identify_and_reclassify_workbased(survey_tour)
identify_and_reclassify_workbased(daysim_tour)

print('Grouping and Writing')
outfile = r'D:\TIM3\ModeTripsByPurpToCBD_Peach0315_Raw.xlsx'
writer = pd.ExcelWriter(outfile)
pivot(survey_tour, 'tmodetp', 'pdpurp', 'toexpfac').to_excel(writer, 'Survey')
pivot(daysim_tour, 'tmodetp', 'pdpurp', 'toexpfac').to_excel(writer, 'DaySim')
writer.close()
print('Done')

#for p in range(1, 8):
#    print(p)
#    survey_tour_p = survey_tour.query('pdpurp == @p')
#    daysim_tour_p = daysim_tour.query('pdpurp == @p')
    
#    print('Grouping')
#    survey_tours_by_mode = survey_tour_p.groupby('tmodetp').sum()['toexpfac']
#    daysim_tours_by_mode = daysim_tour_p.groupby('tmodetp').sum()['toexpfac']

#    mode_shares = pd.DataFrame(np.zeros((9, 2)), columns = ['Survey', 'DaySim'], index = range(1, 10))
#    mode_shares['Survey'] += survey_tours_by_mode# / survey_tours_by_mode.sum()
#    mode_shares['DaySim'] += daysim_tours_by_mode# / daysim_tours_by_mode.sum()
#    #mode_shares = pd.DataFrame(mode_shares)
#    mode_shares.to_csv(r'D:\TIM3\ModeTripsToCoreCBD_Y0309_pdpurp=%d.csv'%(p))

#print('WorkBased')
#print('Grouping')
#survey_tours_by_mode = survey_workbased.groupby('tmodetp').sum()['toexpfac']
#daysim_tours_by_mode = daysim_workbased.groupby('tmodetp').sum()['toexpfac']

#mode_shares = pd.DataFrame(np.zeros((9, 2)), columns = ['Survey', 'DaySim'], index = range(1, 10))
#mode_shares['Survey'] += survey_tours_by_mode# / survey_tours_by_mode.sum()
#mode_shares['DaySim'] += daysim_tours_by_mode# / daysim_tours_by_mode.sum()
#mode_shares.to_csv(r'D:\TIM3\ModeTripsToCoreCBD_Y0309_WorkBased.csv')