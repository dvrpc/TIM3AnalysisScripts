import pandas as pd
import numpy as np

pnr_node_file = r'D:\TIM3.1\DaySimLab\scenario\inputs\DVRPC_p_rNodes.dat'
pnr = pd.read_csv(pnr_node_file, '\t', index_col = 0)

pnr['nearest_parcel_id'] = 80056*np.ones(pnr.shape[0], int)
pnr['nearest_stoparea_id'] = 1103*np.ones(pnr.shape[0], int)

pnr.to_csv(pnr_node_file, '\t')
print('Done')