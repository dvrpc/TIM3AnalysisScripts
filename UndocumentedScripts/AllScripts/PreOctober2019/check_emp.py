import pandas as pd
import os

wd = os.path.split(__file__)[0]
fp = os.path.join(wd, '_DVRPC_prec.dat')

per = pd.read_table(fp, ' ')

print('Go')