import pandas as pd
import numpy as np
import VisumPy.helpers as h

Visum.Log(20480, 'Reading VISUM Data')
zones = np.array(h.GetMulti(Visum.Net.Zones, 'No'))
names = np.array(h.GetMulti(Visum.Net.Zones, 'Name'))

threshold = 0.5
dis = pd.DataFrame(h.GetMatrix(Visum, 402), zones, zones)
under_threshold = (dis < threshold)

Visum.Log(20480, 'Reading External Data')
homeloc_file = r'D:\TIM3\CCUCEmpHomeLocations.csv'
ccuc_workers_by_hhtaz = pd.read_csv(homeloc_file, index_col = 0)
pnr_under_threshold = under_threshold.loc[ccuc_workers_by_hhtaz.index, 90000:90300]

Visum.Log(20480, 'Multiplying')
CCUCWorkersWithinPnRLots = pnr_under_threshold.T.dot(ccuc_workers_by_hhtaz)

Visum.Log(20480, 'Writing')
outfile = r'D:\TIM3\CCUCWorkersWithinPnRLotsHalfMile.csv'
CCUCWorkersWithinPnRLots.to_csv(outfile)

Visum.Log(20480, 'Done')