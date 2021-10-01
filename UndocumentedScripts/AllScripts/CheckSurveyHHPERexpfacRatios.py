import pandas as pd
import numpy as np
import os
from collections import OrderedDict

hh_file = r'B:\model_development\TIM_3.1\scenario\DaySimSummaries\data\dvrpc_hrecx4.dat'
hh = pd.read_csv(hh_file, ',')

per_file = r'B:\model_development\TIM_3.1\scenario\DaySimSummaries\data\dvrpc_precx5.dat'
per = pd.read_csv(per_file, ' ')

hhper = hh.merge(per, on = 'hhno')
hhper['weight_ratio'] = hhper['psexpfac'] / hhper['hhexpfac']

person_types = list(hhper['pptyp'].value_counts().sort_index().index)
ratios = OrderedDict()

tol = 1e-3

for pptyp in person_types:
    print(pptyp)
    r = hhper.query('pptyp == @pptyp')['weight_ratio']
    if abs(r.min() - r.max()) < tol:
        ratios[pptyp] = r.mean()
    else:
        ratios[pptyp] = np.nan

ratios = pd.Series(ratios)

pop_hh = hhper.groupby('pptyp').sum()['hhexpfac'].sort_index()
pop_per = hhper.groupby('pptyp').sum()['psexpfac'].sort_index()

results = OrderedDict()
results['Per-HH Weight Ratios'] = ratios
results['Population using HH Weights'] = pop_hh
results['Population using Per Weights'] = pop_per
pd.DataFrame(results).to_csv(r'D:\HHPerWeightRatio.csv')

print('Done')