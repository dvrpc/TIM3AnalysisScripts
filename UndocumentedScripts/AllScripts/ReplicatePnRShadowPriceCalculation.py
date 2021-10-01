from __future__ import division
import pandas as pd
import numpy as np
from scipy.stats.distributions import poisson
import os



timeSpread = 5
minInDay = 1440

StepSize = 0.09524
MaximumPenalty = 10

sp_file = r'D:\TIM3.1\CalibrationApril2021\scenario\working\park_and_ride_shadow_prices.txt'
pnr_file = r'D:\TIM3.1\CalibrationApril2021\scenario\inputs\DVRPC_p_rNodes.dat'

def min2str(minute):
    if minute < 10:
        return '000' + str(minute)
    elif minute < 100:
        return '00' + str(minute)
    elif minute < 1000:
        return '0' + str(minute)
    else:
        return str(minute)

def DetermineShadowPrice(previousShadowPrice, maxLoad, capacity):
    global StepSize, MaximumPenalty

    shadowPrice = np.where((maxLoad > 0) & (capacity > 0),
                           (1 - StepSize)*previousShadowPrice + StepSize*MaximumPenalty*(1-poisson.cdf(capacity, maxLoad)),
                           (1 - StepSize)*previousShadowPrice)

    return shadowPrice

sp = pd.read_csv(sp_file, '\t')
pnr = pd.read_csv(pnr_file, '\t', index_col = 0)

sp['Capacity'] = sp['NODEID'].map(pnr['Capacity'])

print('Calculating Shadow Prices')

shadowPrices = pd.DataFrame(np.zeros((180, minInDay)), range(1, 181), range(minInDay))

for t in range(1, minInDay):
    if t % 60 == 0:
        print('Hour {}'.format(t//60))
    maxLoad = np.zeros_like(sp.index, dtype = float)
    for j in range(max(t - timeSpread, 1), min(t + timeSpread, minInDay)):
        maxLoad = np.where(sp['PRLOAD' + min2str(j-1)] > maxLoad, sp['PRLOAD' + min2str(j-1)], maxLoad)
    shadowPrices[t-1] = DetermineShadowPrice(sp['PRICE' + min2str(t-1)], sp['EXLOAD' + min2str(t-1)] + maxLoad, sp['Capacity'])


print('Go')