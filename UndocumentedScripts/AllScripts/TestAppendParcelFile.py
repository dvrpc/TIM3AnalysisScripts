import pandas as pd
import numpy as np

parcel_file = r'D:\TIM3.1\DaySimLab\scenario\inputs\parcels_buffered.dat'
delimiter = ' '
parcel = pd.read_csv(parcel_file.replace('.dat', ' - Copy.dat'), delimiter)

pnr2taz_file = r'D:\ref\pnr2taz.csv'
pnr2taz = pd.read_csv(pnr2taz_file, index_col = 2)['TAZ2']

i = parcel['parcelid'].max()
(M, N) = parcel.shape

pnr_file = r'D:\TIM3.1\DaySimLab\scenario\inputs\DVRPC_p_rNodes.dat'
pnr = pd.read_csv(pnr_file, '\t')

new_lines = []
print('Appending')
for lot in pnr.index:
    i += 1
    new_row = np.zeros(N, int)
    new_row[0] = pnr.loc[lot, 'ZoneID'] + 200000
    new_row[1] = pnr.loc[lot, 'Xcoord']
    new_row[2] = pnr.loc[lot, 'YCoord']
    new_row[4] = pnr.loc[lot, 'ZoneID']
    parcel.loc[i] = new_row

print('Writing')
parcel.to_csv(parcel_file, delimiter, index = False)

print('Done')