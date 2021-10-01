import pandas as pd
import numpy as np

#Read in trip file and query for origin purpose is home and destination purpose is change mode
trip_file = r'D:\TIM3\DSOutputsYoshi0621\_trip_2.dat'
trip = pd.read_csv(trip_file, '\t').query('opurp == 0 and dpurp == 10')

#Get list of PnR zones with demand
pnr_zones = trip.groupby('dtaz').sum()['trexpfac'].sort_index().index

#Group by destation TAZ (pnr lot) and list all MAZs that are associated with that (should only be one)
zone2maz = pd.Series(np.zeros_like(pnr_zones), pnr_zones)
c = 0
for lot in pnr_zones:
    pnr_mazs = list(trip[['dtaz', 'dpcl', 'trexpfac']].query('dtaz == @lot').groupby('dpcl').count()['trexpfac'].index)
    if len(pnr_mazs) == 1:
        zone2maz.loc[lot] = pnr_mazs[0]
    else:
        print(lot, pnr_mazs)
        c += 1

if c == 0:
    zone2maz.to_csv(r'D:\TIM3\DSOutputsYoshi0621\PnRZoneToMAZ.csv')

print('Go')