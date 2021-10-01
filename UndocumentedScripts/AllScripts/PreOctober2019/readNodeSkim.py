from __future__ import division
import os
import numpy as np
import ctypes
from collections import OrderedDict

wd = os.getcwd()
skim_file = os.path.join(wd, 'nodeskims_visum_text.dat')
mz_node_file = os.path.join(wd, 'corr_mznode.dat')
area_file = os.path.join(wd, 'MercerSurroundingMAZ.txt')
subset_file = os.path.join(wd, 'MercerMAZ.txt')

M = 10

area_maz = open(area_file, 'r').read().split('\n')
subset_maz = open(subset_file, 'r').read().split('\n')[:M]

##mz_nodes = OrderedDict()
##mz_node_lines = open(mz_node_file, 'r')
##first_line = True
##for line in mz_node_lines:
##    entry = line.replace('\n', '').split(' ')
##    if first_line:
##        first_line = False
##    else:
##        mz_nodes[entry[0]] = entry[1]

nodes_maz = OrderedDict()
mz_node_lines = open(mz_node_file, 'r')
first_line = True
for line in mz_node_lines:
    entry = line.replace('\n', '').split(' ')
    if first_line:
        first_line = False
    else:
        nodes_maz[entry[1]] = entry[0]

N = len(area_maz)
##M = 700
skim = np.zeros((M, N))

area_index = {}
for i in range(len(area_maz)):
    area_index[area_maz[i]] = i

subset_index = {}
for i in range(len(subset_maz)):
    subset_index[subset_maz[i]] = i

print 'Running Main Loop'

skim_lines = open(skim_file, 'r')
first_line = True
for line in skim_lines:
    entry = line.replace('\n', '').split(' ')
    
    if first_line:
        onode = entry.index('onode')
        dnode = entry.index('dnode')
        feet = entry.index('feet')
        first_line = False

    else:
        if entry[onode] in nodes_maz.keys():
            if nodes_maz[entry[onode]] in subset_maz:
                if entry[dnode] in nodes_maz.keys():
                    if nodes_maz[entry[dnode]] in area_maz:
                        skim[subset_index[nodes_maz[entry[onode]]], area_index[nodes_maz[entry[dnode]]]] = int(entry[feet])
