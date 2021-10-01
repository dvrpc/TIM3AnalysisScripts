import pandas as pd
import os

trip_file = r'T:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\_trip_2.dat'
outfile = r'D:\TIM3\TransitTrips\sub2subNo5.csv'
sa2mode_file = r'D:\ref\sa2mode_w_stops.csv'
sub_tazs_file = r'D:\ref\SubwayTAZs.txt'
maz2taz_file = r'D:\ref\maz2taz.csv'

print('Reading Files')
sa2mode = pd.read_csv(sa2mode_file, index_col = 0)
f = open(sub_tazs_file, 'r')
lines = f.read().split('\n')
sub_tazs = [int(taz) for taz in lines]
f.close()
del lines
maz2taz = pd.read_csv(maz2taz_file, index_col = 0)['TAZ']
trip = pd.read_csv(trip_file, '\t').query('mode == 6')

print('Processing Data')
trip['osa'] = trip['otaz']
trip['dsa'] = trip['dtaz']

trip['otaz'] = trip['opcl'].map(maz2taz)
trip['dtaz'] = trip['dpcl'].map(maz2taz)

sub2sub = trip.query('otaz in @sub_tazs and dtaz in @sub_tazs')
sub2sub['omode'] = sub2sub['osa'].map(sa2mode['MODE'])
sub2sub['dmode'] = sub2sub['dsa'].map(sa2mode['MODE'])
sub2sub['obus_w_sub'] = sub2sub['osa'].map(sa2mode['Bus But Sub In Stop'])
sub2sub['dbus_w_sub'] = sub2sub['dsa'].map(sa2mode['Bus But Sub In Stop'])

print('Writing File')
sub2sub.to_csv(outfile, index = False)

print('Done')