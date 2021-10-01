import pandas as pd
import numpy as np

dvrpc_counties = [34005, 34007, 34015, 34021, 42017, 42029, 42045, 42091, 42101]
trips = np.array(Visum.Net.Matrices.ItemByKey(1).GetValues()) #TIM 2: 2000, TIM 3: 1
counties = pd.Series(np.array(Visum.Net.Zones.GetMultiAttValues("STATE_COUNTY_ID"))[:, 1])
agg = pd.get_dummies(counties)
county_flow = pd.DataFrame(agg.T.dot(trips).dot(agg), agg.columns, agg.columns)
dvrpc = county_flow[dvrpc_counties].loc[dvrpc_counties]

Visum.Log(20480, 'Total: {}'.format(county_flow.sum().sum()))
Visum.Log(20480, 'IC: {}'.format(county_flow.values.trace()))
Visum.Log(20480, 'DVRPC: {}'.format(dvrpc.sum().sum()))
Visum.Log(20480, 'IC: {}'.format(dvrpc.values.trace()))