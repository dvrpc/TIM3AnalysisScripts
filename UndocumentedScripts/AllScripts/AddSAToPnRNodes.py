import pandas as pd
import numpy as np

pnr_node_file = r'D:\TIM3.1\DaySimLab\scenario\inputs\DVRPC_p_rNodes.dat'
pnr = pd.read_csv(pnr_node_file, '\t', index_col = 0)

parcel_file = r'D:\TIM3.1\DaySimLab\scenario\inputs\parcels_buffered.dat'
parcel = pd.read_csv(parcel_file, ' ').query('taz_p > 90000 ').set_index('taz_p')

pnr2sa_file = r'D:\ref\pnr2sa.csv'
pnr2sa = pd.read_csv(pnr2sa_file, index_col = 0)

pnr2maz_file = r'D:\ref\pnr2maz.csv'
pnr2maz = pd.read_csv(pnr2maz_file, index_col = 2)

#pnr['nearest_parcel_id'] = 80056*np.ones(pnr.shape[0], int)
pnr['nearest_parcel_id'] = pnr['ZoneID'] + 200000
#pnr['nearest_parcel_id'] = pnr['ZoneID'].map(pnr2maz['nearest_parcel_id'])
#pnr['nearest_parcel_id'] = pnr['ZoneID'].map(parcel['parcelid'])
pnr['nearest_stoparea_id'] = pnr['ZoneID'].map(pnr2sa['Stop Area'])

maz_sa_pairs = list(zip(pnr['nearest_parcel_id'], pnr['nearest_stoparea_id']))

def should_keep(args):
    global pnr
    global maz_sa_pairs
    return not (args not in maz_sa_pairs and args[0] in list(pnr['nearest_parcel_id']))

parcel = pd.read_csv(r'D:\TIM3.1\DaySimLab\scenario\inputs\parcels_buffered.dat', ' ')
sa = pd.read_csv(r'D:\TIM3.1\DaySimLab\scenario\working\stoparea.tsv', '\t')
            
print('Updating MAZ distances')
maz2sa_file = r'D:\TIM3.1\DaySimLab\scenario\microzonetostopareadistance.dat'
maz2sa = pd.read_csv(maz2sa_file.replace('.dat', ' - Copy (2).dat'), ' ')
#raise Exception
#maz2sa['pairs'] = list(zip(maz2sa['zoneid'], maz2sa['stopareaid']))
#maz2sa['pnr_pair'] = maz2sa['pairs'].apply(lambda x: x in maz_sa_pairs)
#maz2sa['to_keep'] = maz2sa['pairs'].apply(should_keep)
#maz2sa['distance'] = np.where(maz2sa['pnr_pair'], 0, maz2sa['distance'])
#maz2sa = maz2sa.query('to_keep')
#del maz2sa['pairs']
#del maz2sa['pnr_pair']
#del maz2sa['to_keep']
maz2sa['not_pnr'] = maz2sa['zoneid'].apply(lambda x: x not in list(pnr['nearest_parcel_id']))
maz2sa = maz2sa.query('not_pnr')
del maz2sa['not_pnr']
i = maz2sa.index.max()
not_in = []
sa_not_in = []
for lot in pnr.index:
    i += 1
    if pnr.loc[lot, 'nearest_parcel_id'] not in list(parcel['parcelid']):
        not_in.append(str(pnr.loc[lot, 'nearest_parcel_id']))
    #if pnr.loc[lot, 'nearest_stoparea_id'] not in list(sa['taz']):
    #    sa_not_in.append(pnr.loc[lot, 'nearest_stoparea_id'])
    maz2sa.loc[i] = [pnr.loc[lot, 'nearest_parcel_id'], pnr.loc[lot, 'nearest_stoparea_id'], 0]
if len(not_in) + len(sa_not_in) > 0:
    raise KeyError('MAZs: ' + ','.join(not_in) + ', SAs ' + ','.join(sa_not_in))
maz2sa.to_csv(maz2sa_file, ' ', index = False)

pnr.to_csv(pnr_node_file, '\t')
print('Done')