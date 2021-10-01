import pandas as pd
import numpy as np

new_distance = 2000.0

maz2sa_file = r'D:\TIM3.1\CalibrationJune2021\scenario\microzonetostopareadistance.dat'
maz2sa = pd.read_csv(maz2sa_file.replace('.dat', '_PnRZero.dat'), ' ')

pnr_node_file = r'D:\TIM3.1\CalibrationJune2021\scenario\inputs\DVRPC_p_rNodes.dat'
pnr = pd.read_csv(pnr_node_file, '\t', index_col = 0)

maz_sa_pairs = list(zip(pnr['nearest_parcel_id'], pnr['nearest_stoparea_id']))

maz2sa['pairs'] = list(zip(maz2sa['zoneid'], maz2sa['stopareaid']))
maz2sa['pnr_pair'] = maz2sa['pairs'].apply(lambda x: x in maz_sa_pairs)
print(maz2sa['pnr_pair'].value_counts())
maz2sa['distance'] = np.where(maz2sa['pnr_pair'], new_distance, maz2sa['distance'])
del maz2sa['pairs']
del maz2sa['pnr_pair']
maz2sa.to_csv(maz2sa_file, ' ', index = False)

print('Done')