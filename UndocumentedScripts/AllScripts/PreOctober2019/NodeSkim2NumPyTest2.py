import os
import numpy as np
import scipy as sp
import csv
import time

base_path = r'T:\TIM_3.1\190719_FullTest\scenario'
maz2node_file = os.path.join(base_path, 'maz_to_node.csv')
nodeskim_file = os.path.join(base_path, 'nodeskims_visum_text.dat')

#maz2node = {}
#f = open(maz2node_file, 'r')
#reader = csv.reader(f, delimiter = ',')
#for row in reader:
#    maz2node[int(float(row[0]))] = int(float(row[1]))
#f.close()

node2maz = {}
f = open(maz2node_file, 'r')
reader = csv.reader(f, delimiter = ',')
for row in reader:
    node2maz[int(float(row[1]))] = int(float(row[0]))
f.close()

maznodes = list(node2maz.keys())

def get_maz_from_node(node):
    try:
        return node2maz[node]
    except KeyError:
        return np.nan
get_maz_from_node = np.vectorize(get_maz_from_node)

#N = len(maznodes)
#maz_skim = np.zeros((N, N), np.int16)

#f = open(nodeskim_file, 'r')
#nrows = len(f.readlines())-1
#f.close()

f = open(nodeskim_file, 'r')
break_point = 10000000
last_percent = 0

nrows = break_point

reader = csv.DictReader(f, delimiter = ' ')



print('Reading Data')
o = np.empty(nrows)
d = np.empty(nrows)
dist = np.empty(nrows)
i = 0
ts = time.time()
for row in reader:
    o[i] = (row['onode'])
    d[i] = (row['dnode'])
    dist[i] = (row['feet'])
    i += 1
    if i == break_point:
        te = time.time()
        break
#print(nrows/break_point*(te-ts))
te = time.time()
print('Done Reading Data')
print(te - ts)

omaz = get_maz_from_node(o.astype(int))
dmaz = get_maz_from_node(d.astype(int))

#print(omaz[np.isnan(omaz) == False])

valid_onodes = np.invert(np.isnan(omaz))
valid_dnodes = np.invert(np.isnan(dmaz))
valid_odpairs = valid_onodes * valid_dnodes

#mazskim = sp.sparse.coo_matrix(data, (i, j))



print('Go')