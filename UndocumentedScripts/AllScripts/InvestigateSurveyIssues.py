from __future__ import division
import pandas
import numpy
import threading
import os

output_path = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output'

class TableReader(threading.Thread):
    '''
    Class for multi-threading of reading tables into Pandas. The run() function reads the table into `table_dict`

    Parameters
    ----------
    table_dict (dict): Dictionary to add tables to
    name (str): Name of table
    fp (str): Filepath of DaySim outputs
    sep (str): Text delimiter used in file
    '''
    def __init__(self, table_dict, name, fp, sep):
        threading.Thread.__init__(self)
        self.table_dict = table_dict
        self.name = name
        self.fp = fp
        self.sep = sep
        
    def run(self):      
        df = pandas.read_csv(self.fp, self.sep)
        self.table_dict[self.name] = df

names = ['household', 'person', 'tour', 'trip']
fps = []
for name in names:
    fps.append(os.path.join(output_path, '_{}_2.dat'.format(name)))
tables = {}
readers = []
for i in range(len(names)):
    readers.append(TableReader(tables, names[i], fps[i], '\t'))
    readers[i].start()
for reader in readers:
    reader.join()

print('Reading Transit Skim')
skim_file = r'D:\TIM2\AMTransitIVT.csv'
skim = pandas.read_csv(skim_file, index_col = 0)
skim.columns = skim.columns.astype(float)

def get_transit_time(args):
    global skim
    try:
        return skim.loc[args[0], args[1]]
    except KeyError:
        return None

transit_tours = tables['tour'].query('totaz > 0 and tdtaz > 0 and (tmodetp == 6 or tmodetp == 7)')
transit_tours['od'] = list(zip(transit_tours['totaz'], transit_tours['tdtaz']))
transit_tours['AMTransitTime'] = transit_tours['od'].apply(get_transit_time)
transit_tours['Invalid'] = (transit_tours['AMTransitTime'] == 999999)
#invalid_tours = transit_tours.query('Invalid')

transit_tours['tourid'] = list(zip(transit_tours['hhno'], transit_tours['pno'], transit_tours['day'], transit_tours['tour']))

transit_tour_trips = transit_tours.merge(tables['trip'], on = ['hhno', 'pno', 'day', 'tour'])
transit_tour_trips['tourid'] = list(zip(transit_tour_trips['hhno'], transit_tour_trips['pno'], transit_tour_trips['day'], transit_tour_trips['tour']))
trips_by_tour_and_mode = transit_tour_trips.groupby(['tourid', 'mode']).count()['trexpfac'].reset_index().pivot('tourid', 'mode', 'trexpfac').fillna(0)
trips_by_tour_and_mode['Auto'] = trips_by_tour_and_mode[3] + trips_by_tour_and_mode[4] + trips_by_tour_and_mode[5]
trips_by_tour_and_mode['Total'] = trips_by_tour_and_mode.sum(1)

for i in range(1, 10):
    transit_tours['mode%d'%(i)] = transit_tours['tourid'].map(trips_by_tour_and_mode[i])
transit_tours['auto_trips'] = transit_tours['tourid'].map(trips_by_tour_and_mode['Auto'])
transit_tours['n_trips'] = transit_tours['tourid'].map(trips_by_tour_and_mode['Total'])

invalid_tours = transit_tours.query('Invalid')

#probably_not_transit = transit_tours.query('mode6 == 1 and auto_trips > 1')
#print(probably_not_transit.shape[0])
#print(transit_tours.shape[0])
wt = transit_tours.query('tmodetp == 6 and not Invalid')
print('Total: {}'.format(wt.shape[0]))
for i in range(5):
    print('{0}: {1}'.format(i, wt.query('mode6 == 1 and auto_trips >= @i').shape[0]))



print('Go')