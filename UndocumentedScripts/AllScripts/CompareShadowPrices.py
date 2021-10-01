import pandas as pd
import numpy as np

sp0 = pd.read_csv(r'D:\TIM3\park_and_ride_shadow_prices.txt', '\t')
sp1 = pd.read_csv(r'D:\TIM3.1\CalibrationJuly2021\scenario\working\park_and_ride_shadow_prices.txt', '\t')

p0 = np.zeros((180, 1440))
l0 = np.zeros((180, 1440))
p1 = np.zeros((180, 1440))
l1 = np.zeros((180, 1440))

for i in range(1440):
    if i == 0:
        t = '0000'
    else:
        t = (3 - int(np.log10(i)))*'0' + str(i)

    p0[:, i] = sp0['PRICE' + t]
    l0[:, i] = sp0['PRLOAD' + t]
    p1[:, i] = sp1['PRICE' + t]
    l1[:, i] = sp1['PRLOAD' + t]

print(np.average(p0, weights = l0))
print(np.average(p1, weights = l1))