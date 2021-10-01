from calibration_util import *
from subprocess import Popen

outfile = r'D:\TIM3\ModeTripsSubwayCorridorOrigVsUpdated.csv'

tables = {}
names = ['survey', 'original', 'updated']
fps = [r'B:\model_development\TIM_3.1\scenario\DaySimSummaries\data\dvrpc_tripx5.dat',
       r'B:\model_development\TIM_3.1_OriginalCoefficients\scenario\Output\_trip_2.dat',
       r'B:\model_development\TIM_3.1\scenario\Output\_trip_2.dat']
seps = [' ', '\t', '\t']

readers = []
for i in range(len(fps)):
    readers.append(TableReader(tables, names[i], fps[i], seps[i]))
    readers[i].start()

for reader in readers:
    reader.join()

subway_taz_file = r'D:\ref\SubwayTAZs.txt'
f = open(subway_taz_file, 'r')
lines = f.read().split('\n')
f.close()
subway_tazs = [int(line) for line in lines]

def get_mode_trips(trip_file, qry = None):
    if qry:
        trip_file = trip_file.query(qry)
    return trip_file[['mode', 'trexpfac']].groupby('mode').sum()['trexpfac']

def get_mode_tours(tour_file, qry = None):
    if qry:
        tour_file = tour_file.query(qry)
    return tour_file[['tmodetp', 'toexpfac']].groupby('tmodetp').sum()['toexpfac']

qry = 'otaz in @subway_tazs and dtaz in @subway_tazs and travdist >= 2'
survey_mode_trips = get_mode_trips(tables['survey'], qry)
original_mode_trips = get_mode_trips(tables['original'], qry)
updated_mode_trips = get_mode_trips(tables['updated'], qry)

pd.DataFrame({'survey': survey_mode_trips,
              'original': original_mode_trips,
              'updated': updated_mode_trips}).to_csv(outfile)
Popen(outfile, shell = True)