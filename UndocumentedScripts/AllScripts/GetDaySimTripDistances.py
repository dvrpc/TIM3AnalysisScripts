import numpy as np
import pandas as pd

zones = np.array(Visum.Net.Zones.GetMultiAttValues("No"))[:, 1]
def GetMtx(no):
    '''
    Reads a matrix into a Pandas data frame
    '''
    global zones
    return pd.DataFrame(np.array(Visum.Net.Matrices.ItemByKey(no).GetValues()), index = zones, columns = zones)

dis = {}
dis['0000'] = GetMtx(401)
dis['0600'] = GetMtx(402)
dis['1000'] = GetMtx(403)
dis['1500'] = GetMtx(404)
dis['1900'] = GetMtx(405)

autrips = {}
autrips['0000'] = GetMtx(101)
autrips['0600'] = GetMtx(102)
autrips['1000'] = GetMtx(103)
autrips['1500'] = GetMtx(104)
autrips['1900'] = GetMtx(105)

atl = pd.Series(np.empty(5), index = ['0000', '0600', '1000', '1500', '1900'])
for tod in atl.index:
    atl.loc[tod] = np.average(dis[tod], weights = autrips[tod])
    Visum.Log(20480, tod + ': {}'.format(atl.loc[tod]))