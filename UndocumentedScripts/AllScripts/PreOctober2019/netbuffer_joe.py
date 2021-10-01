from scipy.sparse import csr_matrix
import numpy as np
import pandas as pd
import time
from math import exp
from collections import OrderedDict

def buffer(dist, bdist, boffs, decay):
    return min(1, (1 + exp(decay - 0.5 + boffs/5280))/(1 + exp(decay*(dist/bdist*0.5 - boffs/5280))))

def buffer1(dist):
    return buffer(dist, 660, 2640, 0.76)

def buffer2(dist):
    return buffer(dist, 1320, 2640, 0.76)

t0 = time.time()

print('Reading MAZ data')
maz_file = r'Y:\TIM_3.1\DVRPC_ABM_Github\Tools\PopSim\0_Input\DVRPC_parcelbase.dat'
maz_data = pd.read_csv(maz_file, index_col = 0, delimiter = ' ')

t0a = time.time()
print(t0a - t0)

print('Reading MAZ-node correspondance')
maz2node_file = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\corr_mznode.dat'
maz2node = pd.read_csv(maz2node_file, index_col = None, delimiter = ' ')#['node_id']

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

t3 = time.time()
print(t3 - t2)

print('Getting MAZ skim shape')
df['nomazs'] = df['omazs'].apply(len)
df['ndmazs'] = df['dmazs'].apply(len)
df['nmazpairs'] = df['nomazs'] * df['ndmazs']

t4 = time.time()
print(t4 - t3)

print('Creating MAZ skim')
mazskim = OrderedDict()
omaz = np.hstack(df['omazs'])
dmaz = np.hstack(df['dmazs'])
#dists = np.repeat(df['feet'], df['nmazpairs'])

t5 = time.time()
print(t5-t4)

#raise Exception

#print('Creating node lists')
#df['onode_list'] = df['onode'].apply(lambda x: [x])
#df['dnode_list'] = df['dnode'].apply(lambda x: [x])

#t2 = time.time()
#print(t2 - t1)

#print('Getting list of accesible destination nodes for each origin node')
#oacc = df[['onode', 'dnode_list']].groupby('onode').sum()

#t3 = time.time()
#print(t3 - t2)

#print('Getting list of accesible origin nodes for each destination node')
#dacc = df[['dnode', 'onode_list']].groupby('dnode').sum()

#t4 = time.time()
#print(t4 - t3)

#raise Exception

#print('Creating Buffer 1')
#df['buffer1'] = df['feet'].apply(buffer1)

#t2 = time.time()
#print(t2-t1)

#print('Creating Buffer 2')
#df['buffer2'] = df['feet'].apply(buffer2)

#t3 = time.time()
#print(t3-t2)

#print('Getting MAZ OD info')
#N = maz_data.shape[0]
#maz_od = pd.DataFrame()
#maz_od['omaz'] = np.repeat(maz_data.index, N)
#maz_od['dmaz'] = N*maz_data.index.tolist(N)




#raise Exception
#print('Reshaping into sparse matrix')
#skim = csr_matrix((df['buffer'], (df['onode'], df['dnode'])))



print('Done')