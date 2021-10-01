import VisumPy.helpers as h
import pandas as pd
import numpy as np

matno = 8004
outfile = r'D:\TIM3\TIM31HTrk_NJTPK4to5FB.csv'

order = [42101, 42045, 42029, 42091, 42017,
         34021, 34005, 34007, 34015,
         42071, 42011, 42077, 42095,
         34041, 34019, 34035, 34023, 34025, 34029,
         34001, 34009, 34011, 34033,
         10003, 24015, 0]

trip_table = h.GetMatrix(Visum, matno)
counties = h.GetMulti(Visum.Net.Zones, "STATE_COUNTY_ID")
agg = pd.get_dummies(counties)
county_flow = pd.DataFrame(agg.T.values.dot(trip_table).dot(agg.values),
                           agg.columns, agg.columns)
county_flow.loc[order].T.loc[order].T.to_csv(outfile)