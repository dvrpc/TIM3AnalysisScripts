import pandas as pd
import numpy as np
import os

parcel_file = r'R:\Model_Development\TIM_3.1\scenario\inputs\parcels_buffered.dat'
parcel = pd.read_csv(parcel_file, ' ', index_col = 0)
parcel['CoreCBD'] = ((parcel['hh_1'] + parcel['emptot_1']) > 20000)

survey_hh_file = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_household_2.dat'
survey_per_file = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_person_2.dat'
survey_tour_file = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_tour_2.dat'

base_path = r'Y:\TIM_3.1\DVRPC_ABM_Template\scenario\output'
daysim_hh_file = os.path.join(base_path , '_household_2.dat')
daysim_per_file = os.path.join(base_path , '_person_2.dat')
daysim_tour_file = os.path.join(base_path, '_tour_2.dat')

def separate_workbased(per, tour):
    print(tour.shape[0])
    tour = per.merge(tour, on = ['hhno', 'pno'])
    #tour['WorkBased'] = (tour['pwpcl'] == tour['topcl'])
    tour['WorkBased'] = (tour['parent'] > 0)
    work_based = tour.query('WorkBased == True')
    not_work_based = tour.query('WorkBased == False')
    print(work_based.shape[0])
    print(not_work_based.shape[0])
    return (work_based, not_work_based)

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
(survey_workbased, survey_tour) = separate_workbased(survey_per, survey_tour)
(daysim_workbased, daysim_tour) = separate_workbased(daysim_per, daysim_tour)

for p in range(1, 8):
    print(p)
    survey_tour_p = survey_tour.query('pdpurp == @p')
    daysim_tour_p = daysim_tour.query('pdpurp == @p')
    
    print('Grouping')
    survey_tours_by_mode = survey_tour_p.groupby('tmodetp').sum()['toexpfac']
    daysim_tours_by_mode = daysim_tour_p.groupby('tmodetp').sum()['toexpfac']

    mode_shares = pd.DataFrame(np.zeros((9, 2)), columns = ['Survey', 'DaySim'], index = range(1, 10))
    mode_shares['Survey'] += survey_tours_by_mode# / survey_tours_by_mode.sum()
    mode_shares['DaySim'] += daysim_tours_by_mode# / daysim_tours_by_mode.sum()
    #mode_shares = pd.DataFrame(mode_shares)
    mode_shares.to_csv(r'D:\TIM3\ModeTripsToCoreCBD_Y0309_pdpurp=%d.csv'%(p))

print('WorkBased')
print('Grouping')
survey_tours_by_mode = survey_workbased.groupby('tmodetp').sum()['toexpfac']
daysim_tours_by_mode = daysim_workbased.groupby('tmodetp').sum()['toexpfac']

mode_shares = pd.DataFrame(np.zeros((9, 2)), columns = ['Survey', 'DaySim'], index = range(1, 10))
mode_shares['Survey'] += survey_tours_by_mode# / survey_tours_by_mode.sum()
mode_shares['DaySim'] += daysim_tours_by_mode# / daysim_tours_by_mode.sum()
mode_shares.to_csv(r'D:\TIM3\ModeTripsToCoreCBD_Y0309_WorkBased.csv')

print('Done')