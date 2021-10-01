import pandas as pd
import numpy as np
import os

print('Reading reference files')
taz_ref_file = r'D:\ref\taz2sa_mode.xlsx'
df = pd.read_excel(taz_ref_file)

maz2taz_file = r'D:\ref\maz2taz.csv'
maz2taz = pd.read_csv(maz2taz_file, index_col = 0)['TAZ']

print('Identifying subway-accessible TAZs')
subway_tazs = list(df.query('has_sub == 1')['$CONNECTOR:ZONENO'].value_counts().sort_index().index)

for i in range(2, 6):
    print('COMMENCE THE PROCESSING OF FILE NUMBER %d'%(i))
    infile = r'D:\TIM3\TransitTrips\TransitTripsWithSubBusIVT_WalkWt10_DaySim1208_No%d.csv'%(i)
    outfile = r'D:\TIM3\TransitTrips\sub2subTAZNo%d.csv'%(i)
    data = pd.read_csv(infile)
    data['osa'] = data['otaz']
    data['dsa'] = data['dtaz']
    data['otaz'] = data['opcl'].map(maz2taz)
    data['dtaz'] = data['dpcl'].map(maz2taz)
    data.query('otaz in @subway_tazs and dtaz in @subway_tazs').to_csv(outfile, index = False)

print('Done')