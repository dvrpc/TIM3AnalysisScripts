import pandas as pd
import os
from collections import OrderedDict

fp = r'T:\TIM_3.1\200504_LowerOtherTours\scenario\Output\_tour_2.dat'
df = pd.read_csv(fp, '\t')

data = OrderedDict()
data['ii'] = df.query('totaz < 50000 and tdtaz < 50000')
data['ie'] = df.query('totaz < 50000 and tdtaz >= 50000 and tdtaz < 60000')
data['ei'] = df.query('tdtaz < 50000 and totaz >= 50000 and totaz < 60000')
data['ee'] = df.query('totaz >= 50000 and totaz < 60000 and tdtaz >= 50000 and tdtaz < 60000')

output = pd.DataFrame()
for flow in data:
    output[flow] = data[flow].groupby('pdpurp').sum()['toexpfac']

print(output)