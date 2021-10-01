import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr

infile = r'D:\TIM3\PnRUtilitiesWithTimeCheck0514.dat'
df = pd.read_csv(infile, '\t')

#queries = ['ttc <= 6', 'ttc > 6']
#for query in queries:
#    data = df.query(query)
#    print(data['timediff'].describe())

r = pearsonr(df['ttc'], abs(df['timediff']))
rho = spearmanr(df['ttc'], abs(df['timediff']))

plt.scatter(df['ttc'], -(df['timediff']), color = 'k', s = 1, alpha = 0.3)
plt.grid(True)
plt.xlabel('Travel Time From Skims')
plt.ylabel('Time Difference')
#plt.title('$r={0}$\n$\rho={1}$'.format(r[0], rho[0]))
plt.show()

print('Go')