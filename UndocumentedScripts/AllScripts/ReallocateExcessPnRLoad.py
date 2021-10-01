import pandas as pd
import numpy as np

tour_file = r'D:\TIM3.1\DaySimLab\scenario\Output\reallocate\_tour_2.dat'
trip_file = r'D:\TIM3.1\DaySimLab\scenario\Output\reallocate\_trip_2.dat'

print('Reading')
tour = pd.read_csv(tour_file, '\t').query('pdpurp == 7')
trip = pd.read_csv(trip_file, '\t')

tour['tourid'] = list(zip(tour['hhno'], tour['pno'], tour['day'], tour['tour']))
trip['tourid'] = list(zip(trip['hhno'], trip['pno'], trip['day'], trip['tour']))

def get_tour_pnr_info(tourid):
    global trip
    tourtrips = trip[['otaz', 'opurp', 'dpurp', 'deptm', 'arrtm', 'mode', 'tourid']].query('tourid == @tourid')
    pnr_lot = tourtrips.query('opurp == 10 and mode == 6')['otaz']#.iloc[0]
    entry_minute = tourtrips.query('opurp == 10 and mode == 6')['deptm']#.iloc[0]
    exit_minute = tourtrips.query('dpurp == 10 and mode == 6')['arrtm']#.iloc[0]
    return pnr_lot, entry_minute, exit_minute

print('Getting Tour Info')
tour['pnr_info'] = tour['tourid'].apply(get_tour_pnr_info)
print('Unpacking Tour Info')
tour['pnr_lot'] = tour['pnr_info'].apply(lambda x: x[0])
tour['entry_minute'] = tour['pnr_info'].apply(lambda x: x[1])
tour['exit_minute'] = tour['pnr_info'].apply(lambda x: x[2])

print('Done')