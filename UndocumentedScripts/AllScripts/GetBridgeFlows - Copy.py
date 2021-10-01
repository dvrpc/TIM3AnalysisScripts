import pandas as pd
import numpy as np
import os
import threading

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
        df = pd.read_csv(self.fp, self.sep)
        self.table_dict[self.name] = df

def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3

def setminus(lst1, lst2):
    lst3 = [value for value in lst1 if value not in lst2]
    return lst3

def setproduct(lst1, lst2):
    lst3 = [list(od) for od in (np.transpose([np.tile(lst1, len(lst2)), np.repeat(lst2, len(lst1))]))]
    return lst3

def reverse_od(lst):
    return [[od[1], od[0]] for od in lst]

base_path = r'Y:\TIM_3.1\DVRPC_ABM_Template\scenario\Output\Backup'
#base_path = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output'
taz2cpa_file = r'D:\TIM3\taz2cpa.csv'
taz2cpa = pd.read_csv(taz2cpa_file, index_col = 0)['MAINZONENO']
outfile = r'D:\TIM3\BridgeFlowsCore.csv'

#Define OD sets
br_e =   [702, 701, 801, 802, 803, 703, 805, 704, 1901, 804]
br_w =   [109, 101, 509, 107, 114, 115, 401, 113, 103, 110]
br_ew = setproduct(br_e, br_w)
bfww_e = [801, 804, 901, 803, 802, 702, 903, 906, 805, 2001]
bfww_w = [103, 110, 112, 105, 102, 203, 107, 101, 202, 401]
bfww_ew = setproduct(bfww_e, bfww_w)
both_ew = intersection(br_ew, bfww_ew)
br_ew = setminus(br_ew, both_ew)
bfww_ew = setminus(bfww_ew, both_ew)
both_we = reverse_od(both_ew)
br_we = reverse_od(br_ew)
bfww_we = reverse_od(bfww_ew)

raise Exception

#################################################### MAIN SCRIPT ####################################################

print('Reading')
names = ['household', 'person', 'tour', 'trip']
fps = []
for name in names:
    fps.append(os.path.join(base_path, '_{}_2.dat'.format(name)))
tables = {}
readers = []
for i in range(len(names)):
    readers.append(TableReader(tables, names[i], fps[i], '\t'))
    readers[i].start()
for reader in readers:
    reader.join()

print('Merging and Removing Non-DVRPC HH')
tour_qry = 'hhtaz < 50000'
tables['tour']['hhtaz'] = tables['tour']['hhno'].map(tables['household'].set_index('hhno')['hhtaz'])
tour = tables['tour'].query(tour_qry)
tour['tocpa'] = tour['totaz'].map(taz2cpa)
tour['tdcpa'] = tour['tdtaz'].map(taz2cpa)

tourtrip = tables['tour'].merge(tables['trip'], on = ['hhno', 'pno', 'day', 'tour']).query(tour_qry)
tourtrip['ocpa'] = tourtrip['otaz'].map(taz2cpa)
tourtrip['dcpa'] = tourtrip['dtaz'].map(taz2cpa)

print('Creating Queried Tables')
br_wb_tour = tour.query('tocpa in @br_e and tdcpa in @br_w')
br_eb_tour = tour.query('tocpa in @br_w and tdcpa in @br_e')
br_wb_trip = tourtrip.query('ocpa in @br_e and dcpa in @br_w')
br_eb_trip = tourtrip.query('ocpa in @br_w and dcpa in @br_e')
bfww_wb_tour = tour.query('tocpa in @bfww_e and tdcpa in @bfww_w')
bfww_eb_tour = tour.query('tocpa in @bfww_w and tdcpa in @bfww_e')
bfww_wb_trip = tourtrip.query('ocpa in @bfww_e and dcpa in @bfww_w')
bfww_eb_trip = tourtrip.query('ocpa in @bfww_w and dcpa in @bfww_e')

print('Grouping Data')
output = pd.DataFrame(index = list(range(8))+[10])
output['br_wb_tour_purp'] = br_wb_tour.groupby('pdpurp').sum()['toexpfac']
output['br_eb_tour_purp'] = br_eb_tour.groupby('pdpurp').sum()['toexpfac']
output['br_wb_trip_pdpurp'] = br_wb_trip.groupby('pdpurp').sum()['trexpfac']
output['br_eb_trip_pdpurp'] = br_eb_trip.groupby('pdpurp').sum()['trexpfac']
output['br_wb_trip_opurp'] = br_wb_trip.groupby('opurp').sum()['trexpfac']
output['br_eb_trip_opurp'] = br_eb_trip.groupby('opurp').sum()['trexpfac']
output['br_wb_trip_dpurp'] = br_wb_trip.groupby('dpurp').sum()['trexpfac']
output['br_eb_trip_dpurp'] = br_eb_trip.groupby('dpurp').sum()['trexpfac']

output['bfww_wb_tour_purp'] = bfww_wb_tour.groupby('pdpurp').sum()['toexpfac']
output['bfww_eb_tour_purp'] = bfww_eb_tour.groupby('pdpurp').sum()['toexpfac']
output['bfww_wb_trip_pdpurp'] = bfww_wb_trip.groupby('pdpurp').sum()['trexpfac']
output['bfww_eb_trip_pdpurp'] = bfww_eb_trip.groupby('pdpurp').sum()['trexpfac']
output['bfww_wb_trip_opurp'] = bfww_wb_trip.groupby('opurp').sum()['trexpfac']
output['bfww_eb_trip_opurp'] = bfww_eb_trip.groupby('opurp').sum()['trexpfac']
output['bfww_wb_trip_dpurp'] = bfww_wb_trip.groupby('dpurp').sum()['trexpfac']
output['bfww_eb_trip_dpurp'] = bfww_eb_trip.groupby('dpurp').sum()['trexpfac']

print('Writing Output')
output.to_csv(outfile)

print('Done')