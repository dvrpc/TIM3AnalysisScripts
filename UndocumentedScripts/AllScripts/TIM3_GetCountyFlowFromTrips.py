import numpy as np
import pandas as pd
import VisumPy.helpers as h

trips = h.GetMatrix(Visum, 1)
zone2county = np.array(h.GetMulti(Visum.Net.Zones, "STATE_COUNTY_ID"))
agg = pd.get_dummies(zone2county)
agg_trips = pd.DataFrame(agg.T.dot(trips).dot(agg), agg.columns, agg.columns)

outfile = r'D:\TIM3_AggTrips1203.csv'
agg_trips.to_csv(outfile)

Visum.Log(20480, 'Done')