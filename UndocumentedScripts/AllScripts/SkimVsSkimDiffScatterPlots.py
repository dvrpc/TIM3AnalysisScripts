import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

fp = r'D:\TIM3\PnRUtilitiesWithTimeCheck0518.dat'
print('Reading')
df = pd.read_csv(fp, '\t')
print('Plotting')

plt.scatter(df['ttc'], df['timediff'], s = 1, color = 'k', alpha = 0.01)
plt.xlabel('Time from Skims')
plt.ylabel('Time Difference')
plt.grid(True)
plt.show()
plt.clf()

plt.scatter(df['dis'], df['distdiff'], s = 1, color = 'k', alpha = 0.01)
plt.xlabel('Distance from Skims')
plt.ylabel('Distance Difference')
plt.grid(True)
plt.show()
plt.clf()

print('Done')