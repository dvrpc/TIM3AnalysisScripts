import pandas as pd
import os
import numpy as np
from scipy.stats import pearsonr as r

base_fp = r'T:\TIM_3.1\190308_TestNewTruckDistr\scenario\microzonetostopareadistance.dat'
test_fp = r'D:\TIM3\microzonetostopareadistance.dat'

print('Reading Data')
base = pd.read_csv(base_fp, ' ')
test = pd.read_csv(test_fp, ' ')

print('Processing Data')
base['MAZ-SA'] = list(zip(base['zoneid'], base['stopareaid']))
test['MAZ-SA'] = list(zip(test['zoneid'], test['stopareaid']))

data = base.copy()
data['test_dist'] = data['MAZ-SA'].map(test.set_index('MAZ-SA')['distance'])

data = data.dropna(subset = ['test_dist'])
print(r(data['distance'], data['test_dist']))

print('Go')