import pandas as pd
import numpy as np
import time

fp = r'D:\TIM3\Runs\run0\_person_2.dat'
data = pd.read_table(fp)

def AggregateBy(df, col):

    columns = list(df.columns)
    columns.remove(col)

    aggregation_matrix = pd.get_dummies(df[col])
    
    return pd.DataFrame(np.dot(df[columns].T, aggregation_matrix).T, index = aggregation_matrix.columns, columns = columns)

N = 100

t1s = time.time()
for i in range(N):
    data_by_gend = AggregateBy(data[['pgend', 'psexpfac']], 'pgend')
t1e = time.time()

t2s = time.time()
for i in range(N):
    data_by_gend = data[['pgend', 'psexpfac']].groupby('pgend').sum()
t2e = time.time()

print((t1e - t1s)/N)
print((t2e - t2s)/N)