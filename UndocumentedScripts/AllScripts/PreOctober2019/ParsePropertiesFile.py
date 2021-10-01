import os
import pandas as pd
import numpy as np
from collections import OrderedDict

fp = r'M:\Modeling\Model_Development\TIM3.1\Template_Github\DVRPC_ABM\scenario\dvrpc_apply_2015_tnc.properties'
f = open(fp, 'r')
groups = f.read().split('\n\n')
f.close()

outfile = r'D:\TIM3\dvrpc_apply_2015_tnc.xlsx'

properties = OrderedDict()

for group in groups:
    group_data = group.split('\n')
    name = group_data[0].replace('# ', '').replace('#', '')
    N = len(group_data)-1
    df = pd.DataFrame(np.empty((N, 2), str), columns = ['Variable', 'Value'])
    for i in range(N):
        df.loc[i] = group_data[i].replace(' = ', '=').split('=')
    properties[name] = df

print('Go')