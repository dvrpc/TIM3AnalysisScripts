import pandas as pd
import numpy as np
import VisumPy.helpers as h

def classify_district(zone):
    if zone < 4000:
        return 'icp'
    elif zone < 18000:
        return 'iop'
    elif zone < 30000:
        return 'inj'
    elif zone < 53000:
        return 'epa'
    elif zone < 56000:
        return 'enj'
    elif zone < 58000:
        return 'esj'
    elif zone < 60000:
        return 'eot'
    elif zone < 95000:
        return 'pnr'
    elif zone < 100000:
        return 'phl'
    else:
        return 'ext'

fb = h.GetMatrix(Visum, 2179)
zones = pd.Series(h.GetMulti(Visum.Net.Zones, "No"))
dist = zones.apply(classify_district)
A = pd.get_dummies(dist)
flow = pd.DataFrame(A.T.dot(fb).dot(A), A.columns, A.columns)

outfile = r'D:\TIM3\WB_WW_AM_FlowBundle.csv'
flow.to_csv(outfile)
Visum.Log(20480, 'Done')