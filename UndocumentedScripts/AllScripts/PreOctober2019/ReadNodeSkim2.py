from scipy.sparse import csr_matrix
import numpy as np
import pandas as pd
import time

def buffer(dist):
    return np.exp(-((dist/5280)**2)/2)

t0 = time.time()

print('Reading file')
fp = r'T:\TIM_3.1\190802_FullTest\scenario\nodeskims_visum_text.dat'
df = pd.read_csv(fp, delimiter = ' ')

t1 = time.time()
print(t1-t0)

print('Creating Buffer')
df['buffer'] = df['feet'].apply(buffer)

t2 = time.time()
print(t2-t1)

print('Reshaping into sparse matrix')
skim = csr_matrix((df['buffer'], (df['onode'], df['dnode'])))

t3 = time.time()
print(t3-t2)

print('Done')