import pandas as pd
import numpy as np
import os
import time

ts = time.time()

base_path = r'D:\TIM3\DVRPC_Github_Outputs'
tour_file = os.path.join(base_path, '_tour_2.dat')
trip_file = os.path.join(base_path, '_trip_2.dat')

t0 = time.time()
print('Reading files')
tour = pd.read_csv(tour_file, sep = '\t')
print('Tour file read: %d rows'%(tour.shape[0]))
trip = pd.read_csv(trip_file, sep = '\t')
print('Trip file read: %d rows'%(trip.shape[0]))

t1 = time.time()
print(t1 - t0)

#Create variables for keeping track of corrections
tour['pnr_correction'] = np.zeros_like(tour.index)
trip['pnr_correction'] = np.zeros_like(trip.index)
trip['transit2walk_correction'] = np.zeros_like(trip.index)

print('=====CORRECTING FOR PARK AND RIDE TRIPS IN PHILADELPHIA=====')
print('Identifying tours to fix')
phila2cc_pnr = tour.query('tmodetp == 7 and totaz < 2400 and tdtaz < 400')
tofix = pd.Series(np.ones_like(phila2cc_pnr.index).astype(bool),
                  index = list(zip(phila2cc_pnr['hhno'], phila2cc_pnr['pno'], phila2cc_pnr['day'], phila2cc_pnr['tour'])))

trip['hhperdaytour'] = list(zip(trip['hhno'], trip['pno'], trip['day'], trip['tour'])) #Combine tour ID fields into single attribute
trip['tofix'] = trip['hhperdaytour'].map(tofix).fillna(False)

depart_auto_leg = trip.query('tofix and mode != 6 and dpurp == 10')
depart_transit_leg = trip.query('tofix and mode == 6 and opurp == 10')
return_transit_leg = trip.query('tofix and mode == 6 and dpurp == 10')
return_auto_leg = trip.query('tofix and mode != 6 and opurp == 10')

print('Correcting tour data')
tour.loc[phila2cc_pnr.index, 'tmodetp'] = 6
tour.loc[phila2cc_pnr.index, 'pnr_correction'] += 1

print('Correcting trip data')
trip.loc[depart_transit_leg.index, 'otaz'] = list(depart_auto_leg['otaz'])
trip.loc[depart_transit_leg.index, 'opurp'] = list(depart_auto_leg['opurp'])
trip.loc[depart_transit_leg.index, 'pnr_correction'] = 1
trip.loc[return_transit_leg.index, 'dtaz'] = list(return_auto_leg['dtaz'])
trip.loc[return_transit_leg.index, 'dpurp'] = list(return_auto_leg['dpurp'])
trip.loc[return_transit_leg.index, 'pnr_correction'] = 1
trip.loc[depart_auto_leg.index] = np.nan
trip.loc[return_auto_leg.index] = np.nan
trip = trip.dropna()

print('Cleaning Up')
del trip['hhperdaytour']
del trip['tofix']

#for col in tour.columns:
#    try:
#        tour[col] = tour[col].astype(int)
#    except Exception:
#        continue

#for col in trip.columns:
#    try:
#        trip[col] = trip[col].astype(int)
#    except Exception:
#        continue

trip['mode'] = trip['mode'].astype(int)
trip['opurp'] = trip['opurp'].astype(int)
trip['dpurp'] = trip['dpurp'].astype(int)
trip['otaz'] = trip['otaz'].astype(int)
trip['dtaz'] = trip['dtaz'].astype(int)

t2 = time.time()
print(t2 - t1)

print('=====CORRECTING FOR SHORT TRANSIT TRIPS=====')
min_transit_dist = 0.5
short_transit = trip.query('mode == 6 and travdist < @min_transit_dist')
trip.loc[short_transit.index, 'mode'] = 3
trip.loc[short_transit.index, 'transit2walk_correction'] = 1

t3 = time.time()
print(t3 - t2)

print('Writing tour file: %d rows'%(tour.shape[0]))
tour.to_csv(tour_file, sep = '\t', index = False)

t4 = time.time()
print(t4 - t3)

print('Writing trip file: %d rows'%(trip.shape[0]))
trip.to_csv(trip_file, sep = '\t', index = False)

te = time.time()
print(te - t4)
print(te - ts)