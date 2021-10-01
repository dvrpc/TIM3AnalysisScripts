import pandas as pd
import numpy as np
import os
from shutil import copy

remove_invalid = False
remove_likely_auto = False

survey_path = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output'

tour_file = os.path.join(survey_path, '_tour_2.dat')
trip_file = os.path.join(survey_path, '_trip_2.dat')

copy(tour_file.replace('.dat', '_NotCorrected.dat'), tour_file)

tour = pd.read_csv(tour_file, '\t')
trip = pd.read_csv(trip_file, '\t')

print('Reading Transit Skim')
skim_file = r'D:\TIM2\AMTransitIVT.csv'
skim = pd.read_csv(skim_file, index_col = 0)
skim.columns = skim.columns.astype(float)

def get_transit_time(args):
    global skim
    try:
        return skim.loc[args[0], args[1]]
    except KeyError:
        return None

trimmed = pd.read_csv(os.path.join(survey_path, 'trimmed.csv')).dropna()

valid_tours = list(zip(trimmed['hhno'], trimmed['pno'], trimmed['day'], trimmed['tour']))
tour['tourid'] = list(zip(tour['hhno'], tour['pno'], tour['day'], tour['tour']))
tour['NotInTrimmedData'] = ((tour['tourid'].apply(lambda x: x not in valid_tours)) & (tour['tmodetp'] == 7)).astype(int)
tour['tmodetp'] = np.where(tour['NotInTrimmedData'], 9, tour['tmodetp'])


if remove_invalid:
    print('Reclassifying Invalid Transit Times')
    tour['od'] = list(zip(tour['totaz'], tour['tdtaz']))
    tour['AMTransitTime'] = tour['od'].apply(get_transit_time)
    tour['InvalidTransit'] = (((tour['tmodetp'] == 6) | (tour['tmodetp'] == 7)) & (tour['AMTransitTime'] == 999999))
    tour['tmodetp'] = np.where(tour['InvalidTransit'], 9, tour['tmodetp'])

if remove_likely_auto:
    print('Reclassifying Likely SOV Tours')
    tour['tourid'] = list(zip(tour['hhno'], tour['pno'], tour['day'], tour['tour']))
    tourtrip = tour.merge(trip, on = ['hhno', 'pno', 'day', 'tour'])
    tourtrip['tourid'] = list(zip(trip['hhno'], trip['pno'], trip['day'], trip['tour']))
    trips_by_tour_and_mode = tourtrip.groupby(['tourid', 'mode']).count()['trexpfac'].reset_index().pivot('tourid', 'mode', 'trexpfac').fillna(0)
    trips_by_tour_and_mode['Auto'] = trips_by_tour_and_mode[3] + trips_by_tour_and_mode[4] + trips_by_tour_and_mode[5]
    trips_by_tour_and_mode['Total'] = trips_by_tour_and_mode.sum(1)

    for i in range(1, 10):
        tour['mode%d'%(i)] = tour['tourid'].map(trips_by_tour_and_mode[i])
    tour['auto_trips'] = tour['tourid'].map(trips_by_tour_and_mode['Auto'])
    tour['n_trips'] = tour['tourid'].map(trips_by_tour_and_mode['Total'])

    tour['ProbablyAuto'] = ((tour['tmodetp'] == 6) & (tour['mode6'] == 1) & (tour['mode3'] > 1))
    tour['tmodetp'] = np.where(tour['ProbablyAuto'], 9, tour['tmodetp'])

print('Writing')
tour.to_csv(tour_file, '\t')

print('Go')



#transit_tours['tourid'] = list(zip(transit_tours['hhno'], transit_tours['pno'], transit_tours['day'], transit_tours['tour']))

#transit_tour_trips = transit_tours.merge(tables['trip'], on = ['hhno', 'pno', 'day', 'tour'])
#transit_tour_trips['tourid'] = list(zip(transit_tour_trips['hhno'], transit_tour_trips['pno'], transit_tour_trips['day'], transit_tour_trips['tour']))
#trips_by_tour_and_mode = transit_tour_trips.groupby(['tourid', 'mode']).count()['trexpfac'].reset_index().pivot('tourid', 'mode', 'trexpfac').fillna(0)
#trips_by_tour_and_mode['Auto'] = trips_by_tour_and_mode[3] + trips_by_tour_and_mode[4] + trips_by_tour_and_mode[5]
#trips_by_tour_and_mode['Total'] = trips_by_tour_and_mode.sum(1)

#for i in range(1, 10):
#    transit_tours['mode%d'%(i)] = transit_tours['tourid'].map(trips_by_tour_and_mode[i])
#transit_tours['auto_trips'] = transit_tours['tourid'].map(trips_by_tour_and_mode['Auto'])
#transit_tours['n_trips'] = transit_tours['tourid'].map(trips_by_tour_and_mode['Total'])

#transit_tours['ProbablyAuto'] = transit_tours['mode6 == 1 and mode3 > 1']

#transit_tours['To Change'] = (transit_tours['Invalid'] | transit_tours['ProbablyAuto'])
