import pandas
import os
import VisumPy.helpers as h

def UpdateVisumTable(container, filepath, sep = ',', label = ''):
    '''
    Updates values in a Visum table with an input table
    '''
    data = pandas.read_csv(filepath, sep)
    fields = data.columns
    for field in fields:
        try:
            h.SetMulti(container, field + label, data[field])
        except TypeError:
            Visum.Log(20480, field)

scenario_path = Visum.GetPath(69)
parcel_file = os.path.join(scenario_path, 'inputs', 'parcels_buffered.dat')
logsum_file = os.path.join(scenario_path, 'Output', 'aggregate_logsums.{}.dat')
purposes = ['', 'Work', 'School', 'Escort', 'PersBus', 'Shop', 'Meal', 'SocRec']
Visum.Log(20480, 'Updating MAZs')
UpdateVisumTable(Visum.Net.POICategories.ItemByKey(10).POIs, parcel_file, ' ') #

#for i in range(1, 8):
#    UpdateVisumTable(Visum.Net.Zones, logsum_file.format(i), '_' + purposes[i]) #Check if / allowable in field names

Visum.Log(20480, 'Done')