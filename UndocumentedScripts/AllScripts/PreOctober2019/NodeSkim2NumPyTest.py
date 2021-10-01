import os
import numpy as np
import scipy as sp
import csv
import time

base_path = r'T:\TIM_3.1\190719_FullTest\scenario'
maz2node_file = os.path.join(base_path, 'maz_to_node.csv')
nodeskim_file = os.path.join(base_path, 'nodeskims_visum_text.dat')

maz2node = {}
f = open(maz2node_file, 'r')
reader = csv.reader(f, delimiter = ',')
for row in reader:
    maz2node[int(float(row[0]))] = int(float(row[1]))
f.close()

maznodes = list(maz2node.values())

N = len(maz2node.keys())
#maz_skim = np.zeros((N, N), np.int16)

i = []
j = []
data = []

n = 0
max_dist = 0
f = open(nodeskim_file, 'r')
reader = csv.DictReader(f, delimiter = ' ')

nrows = 69417752
last_percent = 0

print('Reading Data')
for row in reader:

    n += 1
    print(n)
    new_percent = int(100*n/nrows)
    if new_percent > last_percent:
        last_percent = new_percent
        print(str(last_percent) + ' %')

    try:
        i += [maznodes.index(int(float(row['onode'])))]
        j += [maznodes.index(int(float(row['dnode'])))]
        data += [maznodes.index(int(float(row['feet'])))]
    except ValueError:
        continue
f.close()
print('Done Reading Data')

mazskim = sp.sparse.coo_matrix(data, (i, j))

#    #max_dist = max(max_dist, float(row['feet']))


#print(n)
#print(N**2)
#print(max_dist)

print('Go')