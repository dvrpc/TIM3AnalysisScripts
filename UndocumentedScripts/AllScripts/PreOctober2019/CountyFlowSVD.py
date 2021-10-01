import os
import pandas as pd
import numpy as np

base_path = os.path.split(__file__)[0]
infile = os.path.join(base_path, 'CountyWorkFlow.csv')
data = pd.read_csv(infile, index_col = None)

global_mean = data[['LOGACS', 'LOGHTS']].values.mean()
global_sd = data[['LOGACS', 'LOGHTS']].values.std()

for col in ['LOGACS', 'LOGHTS']:
    data[col] = (data[col] - data[col].mean()) / data[col].std()

X = data[['LOGACS', 'LOGHTS']].values
(U, S, VT) = np.linalg.svd(X.T)
projection = -np.dot(U.T, X.T).T[:, 0]

data['COMBINED'] = np.exp(projection*global_sd + global_mean) - 1

print(data[['2011-15 ACS', '2012-13 HTS', 'COMBINED']])

print('Go')
