from scipy.sparse import csr_matrix, spdiags
from scipy.special import expit
import numpy as np
import pandas as pd
import time
from numpy import exp
from collections import OrderedDict
from itertools import product
from math import ceil

def buffer(dist, bdist, boffs, decay):
    return np.minimum(1, (1 + np.exp(decay - 0.5 + boffs/5280))/(1 + np.exp(decay*(dist/bdist*0.5 - boffs/5280))))

def buffer1(dist):
    #return buffer(dist, 660, 2640, 0.76)
    dist = 0.05*ceil(20*dist)
    return expit(-8*(dist - 0.5)) if dist <= 1 else 0

def buffer2(dist):
    #return buffer(dist, 1320, 2640, 0.76)
    dist = 0.1*(ceil(10*dist))
    return expit(-4*(dist - 1)) if dist <= 2 else 0

buffer1 = np.vectorize(buffer1)
buffer2 = np.vectorize(buffer2)

def get_od_pairs(args):
    return list(product(args[0], args[1]))

t0 = time.time()

print('Reading MAZ data')
maz_file = r'Y:\TIM_3.1\DVRPC_ABM_Github\Tools\PopSim\0_Input\DVRPC_parcelbase.dat'
maz_data = pd.read_csv(maz_file, index_col = 0, delimiter = ' ')

t0a = time.time()
print(t0a - t0)

print('Reading MAZ-node correspondance')
maz2node_file = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\corr_mznode.dat'
maz2node = pd.read_csv(maz2node_file, index_col = None, delimiter = ' ')

t0b = time.time()
print(t0b - t0a)

print('Reading node skim')
fp = r'T:\TIM_3.1\190802_FullTest\scenario\nodeskims_visum_text.dat'
df = pd.read_csv(fp, delimiter = ' ')

t1 = time.time()
print(t1-t0b)

print('Getting lists of MAZs for each node')
maz2node['id_list'] = maz2node['id'].apply(lambda x: [x])
nodemazs = maz2node[['node_id', 'id_list']].groupby('node_id').sum()['id_list']

t2 = time.time()
print(t2 - t1)

print('Getting MAZ OD Pairs')
df['omazs'] = df['onode'].map(nodemazs)
df['dmazs'] = df['dnode'].map(nodemazs)
del df['onode'], df['dnode']

t2a = time.time()
print(t2a - t2)

print('Getting OD MAZs from OD nodes')
df['odmazs'] = list(zip(df['omazs'], df['dmazs']))
t2b = time.time()
print(t2b-t2a)
df['odmazs'] = df['odmazs'].apply(get_od_pairs)

t2c = time.time()
print(t2c - t2b)
df['odmazs'] = df['odmazs'].apply(np.array)
df['omazs'] = df['odmazs'].apply(lambda x: x[:, 0])
df['dmazs'] = df['odmazs'].apply(lambda x: x[:, 1])
del df['odmazs']
t3 = time.time()
print(t3 - t2c)

print('Getting MAZ skim shape')
df['nmazpairs'] = df['omazs'].apply(len)

t4 = time.time()
print(t4 - t3)

print('Creating MAZ skim')
dists = (1./5280) * np.repeat(df['feet'], df['nmazpairs']).values
omazs = np.hstack(df['omazs'])
dmazs = np.hstack(df['dmazs'])

t4b = time.time()
print(t4b - t4)

print('Creating Buffering Matrices')
b1 = csr_matrix((buffer1(dists), (omazs, dmazs)))[1:, 1:]
b2 = csr_matrix((buffer2(dists), (omazs, dmazs)))[1:, 1:]

t4c = time.time()
print(t4c - t4b)

print('Adding Intra-MAZ Buffer Values')
b1 += spdiags(buffer1(1e-8)*np.ones(b1.shape[0]), [0], b1.shape[0], b1.shape[1])
b2 += spdiags(buffer2(1e-8)*np.ones(b2.shape[0]), [0], b2.shape[0], b2.shape[1])

t5 = time.time()
print(t5-t4c)

print('Buffering Data')
cols_to_buffer = ['sqft_p', 'hh_p', 'stugrd_p', 'stuhgh_p', 'empedu_p', 'empfoo_p', 'empgov_p', 'empind_p', 'empmed_p', 'empofc_p', 'empret_p', 'empsvc_p', 'empoth_p', 'emptot_p', 'parkdy_p', 'parkhr_p']
buffer_1_cols = [col.replace('_p', '_1') for col in cols_to_buffer]
buffer_2_cols = [col.replace('_p', '_2') for col in cols_to_buffer]

t5a = time.time()
buffered_data_1 = pd.DataFrame(b1.dot(maz_data[cols_to_buffer]), index = maz_data.index, columns = buffer_1_cols)
t5b = time.time()
print(t5b - t5a)
buffered_data_2 = pd.DataFrame(b2.dot(maz_data[cols_to_buffer]), index = maz_data.index, columns = buffer_2_cols)
t6 = time.time()
print(t6 - t5b)

print('Writing Buffered Data')
maz_data[buffer_1_cols] = buffered_data_1
maz_data[buffer_2_cols] = buffered_data_2
maz_data.to_csv(r'D:\TIM3\netbuffer_joe_test.csv')

t7 = time.time()
print(t7 - t6)

print('Done')

te = time.time()
print(te - t0)