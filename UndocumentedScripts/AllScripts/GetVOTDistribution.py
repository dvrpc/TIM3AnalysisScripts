from dsa_util import *
import matplotlib.pyplot as plt

fp = r'D:\TIM3.1\200212_FullRunLessSASkimming\ShorterWorkTourLength\scenario\Output\_trip_2.dat'
print('Reading File')
trip = pd.read_csv(fp, '\t')

max_vot = 50
bin_size = 1
trip['$/hr'] = 0.6*trip['vot']
data = trip.query('mode == 6')[['$/hr', 'trexpfac']]
#data = data[data['$/hr'] <= max_vot]
bins = np.arange(0, int(data['$/hr'].max()+1) + bin_size, bin_size)

plt.hist(data['$/hr'], bins = bins, density = True, edgecolor = 'k', facecolor = 'b')
plt.xlabel('$/hr')
plt.xlim(0, max_vot)
plt.show()

print(trip['vot'].max())
print(data['$/hr'].max())
print(np.average(data['$/hr'], weights = data['trexpfac']))

import numpy as np
vots = np.repeat(data['$/hr'], data['trexpfac'])
m = vots.median()
print(m)
print(60/m)