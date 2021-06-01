'''
This script reads in a trip table from VISUM, aggregates it to the county level, and writes a CSV file
'''
import VisumPy.helpers as h
import pandas as pd
import numpy as np

matno = 8004 #Matrix number to aggregate
outfile = r'D:\TIM3\TIM31HTrk_NJTPK4to5FB.csv' #File to write to

#Define county order in which to report the flow
order = [42101, 42045, 42029, 42091, 42017,         #DVRPC PA
         34021, 34005, 34007, 34015,                #DVRPC NJ
         42071, 42011, 42077, 42095,                #Extended PA
         34041, 34019, 34035, 34023, 34025, 34029,  #Extended North Jersey
         34001, 34009, 34011, 34033,                #Extended South Jersey
         10003, 24015, 0]                           #Extended DE/MD and external

#Read in trip table and list of counties for each zone
trip_table = h.GetMatrix(Visum, matno)
counties = h.GetMulti(Visum.Net.Zones, "STATE_COUNTY_ID")

#Aggreate trip table by creating aggregation matrix and implementing the matrix multiplication agg.T * trip_table * agg
agg = pd.get_dummies(counties)
county_flow = pd.DataFrame(agg.T.values.dot(trip_table).dot(agg.values),
                           index = agg.columns, columns = agg.columns)

#Write to file, ordering the rows and columns as specified by `order`
county_flow.loc[order].T.loc[order].T.to_csv(outfile)