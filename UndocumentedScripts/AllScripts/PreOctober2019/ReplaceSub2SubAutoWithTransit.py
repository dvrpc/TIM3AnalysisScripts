import pandas as pd
import numpy as np
import sys

print('Reading Trip File')
trip_file = sys.argv[1]
trip = pd.read_csv(trip_file, '\t')

print('Reading Subway-Accessible MAZs')
subway_maz_file = sys.argv[2]
f = open(subway_maz_file)
lines = f.read().split('\n')
subway_mazs = [int(maz) for maz in lines]
f.close()

print('Reclassifying Mode')
sub2sub = trip[['opcl', 'dpcl', 'mode']].query('opcl in @subway_mazs and dpcl in @subway_mazs and mode in [3, 4, 5]').index
trip.loc[sub2sub, 'mode'] = 6*np.ones_like(sub2sub)

print('Writing Trip File')
trip.to_csv(trip_file, '\t')