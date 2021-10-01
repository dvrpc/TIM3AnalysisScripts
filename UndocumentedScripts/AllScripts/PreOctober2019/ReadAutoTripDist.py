import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
from collections import OrderedDict as od

#fp = r'Y:\TIM_3.1\DVRPC_ABM_VISUM18patch\scenario\AutoTripDists.csv'
#fp = r'R:\Model_Development\TIM_3.1\scenario\AutoTripDists.csv'
#fp = r'T:\TIM_3.1\190802_FullTest\scenario\AutoTripDists.csv'
fp = r'B:\model_development\190821_TIM31DaySimOnly\scenario\AutoTripDists.csv'
df = pd.read_csv(fp, index_col = 0)

taz2side = {}
for i in range(18000):
    taz2side[i] = 1
for i in range(18000, 26000):
    taz2side[i] = 0
for i in range(50000, 53000):
    taz2side[i] = 1
for i in range(53000, 58000):
    taz2side[i] = 0
for i in range(58000, 59000):
    taz2side[i] = 1

df['oside'] = df['otaz'].map(taz2side)
df['dside'] = df['dtaz'].map(taz2side)

df = df.sort_values('dist_diff', ascending = False)
print(df[['hhno', 'tod', 'otaz', 'opcl', 'dtaz', 'dpcl', 'travdist', 'visumdist', 'dist_diff']])

dvrpc = df.query('otaz < 50000 and dtaz < 50000')
df_results = df['dist_diff'].describe(percentiles = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
dvrpc_results = dvrpc['dist_diff'].describe(percentiles = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])

morethan3 = df.query('dist_diff > 3 or dist_diff < -3')
dvrpc_more_than3 = dvrpc.query('dist_diff > 3 or dist_diff < -3')

intrazonal = df.query('otaz == dtaz')
dvrpc_intrazonal = dvrpc.query('otaz == dtaz')

print(morethan3.shape[0] / df.shape[0])
print(dvrpc_more_than3.shape[0] / dvrpc.shape[0])

intrazonal_results = intrazonal['dist_diff'].describe(percentiles = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
dvrpc_intrazonal_results = dvrpc_intrazonal['dist_diff'].describe(percentiles = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])

pd.set_option('display.float_format', lambda x: '%.3f' % x)
results = od()
results['Total'] = df_results
results['Intra-DVRPC'] = dvrpc_results
results['Intrazonal'] = intrazonal_results
results['DVRPC IntraZonal'] = dvrpc_intrazonal_results
results = pd.DataFrame(results)
print(results)


dvrpc_crossings = dvrpc.dropna(subset = [['oside', 'dside']]).query('oside != dside')
print(dvrpc_crossings['dist_diff'].describe())

#density = gaussian_kde(dvrpc['dist_diff'])
#x = np.linspace(dvrpc['dist_diff'].min(), dvrpc['dist_diff'].max(), 1000)
#y = density(x)
#plt.plot(x, y)
#plt.grid(True)
#plt.show()