from calibration_util import *
import matplotlib.pyplot as plt
from scipy.stats import pearsonr as r

names = ['tour', 'trip']
fps = [r'B:\model_development\TIM_3.1\scenario\Output\_tour_2.dat',
       r'B:\model_development\TIM_3.1\scenario\Output\_trip_2.dat']

tables = ReadTables(names, fps, 2*['\t'])

#tourtrip = tables['tour'].merge(tables['trip'], on = ['hhno', 'pno', 'day', 'tour'])
#plt.scatter(tourtrip['tautodist'], tourtrip['travdist'], color = 'k', s = 1, alpha = 0.5)
#plt.grid(True)
#plt.title(r(tourtrip['tautodist'], tourtrip['travdist']))
#plt.show()

tables['trip']['tourid'] = list(zip(tables['trip']['hhno'], tables['trip']['pno'], tables['trip']['day'], tables['trip']['tour']))
total_dist_by_tour = tables['trip'][['tourid', 'travdist']].groupby('tourid').sum()['travdist']
tables['tour']['tourid'] = list(zip(tables['tour']['hhno'], tables['tour']['pno'], tables['tour']['day'], tables['tour']['tour']))
tables['tour']['travdist'] = tables['tour']['tourid'].map(total_dist_by_tour)

tables['tour'] = tables['tour'].query('tmodetp in [3, 4, 5]')
tables['tour']['n'] = tables['tour']['tripsh1'] + tables['tour']['tripsh2']

x = tables['tour']['tautodist']
y = tables['tour']['travdist'] / tables['tour']['n']

plt.scatter(x, y, color = 'k', s = 1, alpha = 0.005)
#plt.grid(True)
plt.xlabel('Distance to Primary Destination')
plt.ylabel('Average Leg Distance')
plt.title(r(x, y))
plt.show()