import pandas as pd
import numpy as np
import os

#base_path = r'D:\TIM3.1\CalibrationApril2021\scenario\Output'
base_path = r'Y:\TIM_3.1\TestPnRShadowPriceConvergence\scenario\Output'
#base_path = r'D:\TIM3.1\TestPnRShadowPriceConvergence\scenario\Output'
outfile = r'D:\TIM3\CCUCEmpHomeLocations.csv'

timestamps = ['2105041916',
              '2105042110',
              '2105042306',
              '2105050100',
              '2105050259',
              '2105050457',
              '2105050700',
              '2105050856',
              '2105051051',
              '2105051249']

ccuc_workers_by_hhtaz = {}
N = len(timestamps)
for i in range(N):
    print('Iter {}'.format(i+1))

    hh_file = os.path.join(base_path, timestamps[i], '_household_2.dat')
    ps_file = os.path.join(base_path, timestamps[i], '_person_2.dat')

    hh = pd.read_csv(hh_file, '\t')
    ps = pd.read_csv(ps_file, '\t')

    qry = '(pwtaz > 0 and pwtaz < 200) or (pwtaz > 1000 and pwtaz < 1200)'
    ccuc_workers = hh[['hhno', 'hhtaz']].merge(ps[['hhno', 'pno', 'pwtaz', 'psexpfac']], on = 'hhno').query(qry)
    ccuc_workers_by_hhtaz['Iter {}'.format(i+1)] = ccuc_workers.groupby('hhtaz').sum()['psexpfac']

print('Writing')
pd.DataFrame(ccuc_workers_by_hhtaz).fillna(0).to_csv(outfile)

print('Done')