import pandas as pd

time_map = {}
for t in range(360):
    time_map[t] = 'NT'
for t in range(360, 600):
    time_map[t] = 'AM'
for t in range(600, 900):
    time_map[t] = 'MD'
for t in range(900, 1140):
    time_map[t] = 'PM'
for t in range(1140, 1440):
    time_map[t] = 'NT'

def classify_time(args):
    global time_map
    deptm = args[0]
    arrtm = args[1]
    half = args[2]
    if half == 2:
        return time_map[deptm]
    else:
        return time_map[arrtm]

tour_file = r'D:\TIM3.1\CenterCityScreenlineCalibration\scenario\Output\_tour_2.dat'
trip_file = r'D:\TIM3.1\CenterCityScreenlineCalibration\scenario\Output\_trip_2.dat'
tour = pd.read_csv(tour_file, '\t')
trip = pd.read_csv(trip_file, '\t')
tourtrip = tour.merge(trip, on = ['hhno', 'pno', 'day', 'tour'])

tourtrip['args'] = list(zip(tourtrip['deptm'], tourtrip['arrtm'], tourtrip['half']))
tourtrip['tod'] = tourtrip['args'].apply(classify_time)

trips_by_pdpurp_tod = tourtrip.groupby(['pdpurp', 'tod']).sum()['trexpfac'].reset_index().pivot('pdpurp', 'tod', 'trexpfac').fillna(0)
print(trips_by_pdpurp_tod)