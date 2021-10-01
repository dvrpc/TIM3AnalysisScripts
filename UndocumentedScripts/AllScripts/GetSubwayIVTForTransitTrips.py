import pandas as pd
import numpy as np
import os
from Util import WriteToTrace

WriteToTrace(Visum, 'Reading Skim')
skim_file = 'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\PuTSkim_6.00-10.00.IVTT(Sub)'
             
StopAreas = np.array(Visum.Net.StopAreas.GetMultiAttValues("No"))[:,1].astype(int)

try:
    Visum.Net.AddMatrix(10000, objectTypeRef=4, MatrixType=4)
except Exception:
    pass

mat = Visum.Net.Matrices.ItemByKey(10000)
mat.Init()
mat.Open(skim_file, ReadAdditive = True)
subivt = pd.DataFrame(np.array(mat.GetValuesFloat()), index = StopAreas, columns = StopAreas)

WriteToTrace(Visum, 'Formatting Skim Data')
subivt = pd.melt(subivt.reset_index(), id_vars = ['index'], value_vars = list(StopAreas))
subivt['od'] = list(zip(subivt['index'], subivt['variable']))
subivt = subivt.set_index('od')['value']

WriteToTrace(Visum, 'Reading Trip File')
trip_file = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\SA_MAZ-SA-v3_WalkWt10_DaySim1208\_trip_2.dat'

trip = pd.read_csv(trip_file, '\t').query('mode == 6 and deptm >= 360 and deptm < 600')

WriteToTrace(Visum, 'Getting Subway IVT For each trip')
trip['od'] = list(zip(trip['otaz'], trip['dtaz']))
trip['sub_ivt'] = trip['od'].map(subivt)
trip['use_sub'] = (trip['sub_ivt'] > 0) & (trip['sub_ivt'] < 999999)

WriteToTrace(Visum, 'Writing Output')
trip.to_csv(r'D:\TIM3\AMTransitTripsWithSubwayUse.csv')

WriteToTrace(Visum, 'Done')